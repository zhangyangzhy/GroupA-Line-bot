import json

import requests
import xmltodict
from bs4 import BeautifulSoup
from linebot.models import CarouselColumn, PostbackTemplateAction, TemplateSendMessage, CarouselTemplate, \
    TextSendMessage

from WPC.News import News
from WPC.NewsConnection import NewsConnection


class NewsProvider:
    def __init__(self, userid, message):
        self.__redis = NewsConnection().connect()
        self.__userid = userid
        self.__message = message
        self.__redis.delete('temp')
        url = 'https://www.news.gov.hk/en/categories/covid19/html/articlelist.rss.xml'
        html = requests.get(url)
        xmlparse = xmltodict.parse(html.text)
        items = xmlparse['rss']['channel']['item']
        count = 0
        for item in items:
            count += 1
            if count == 4:
                break
            # title
            title = item['title']
            bs = BeautifulSoup(item['description'], 'lxml')
            # img
            image = bs.find('img')['src']
            # detail
            content = ''
            contents = bs.findAll('p')
            for paragraph in contents:
                content += paragraph.text
                content += '\n'
            detail = content
            self.__redis.incr('index')
            index = self.__redis.get('index')
            self.__redis.hset('temp', index, json.dumps(News(title, detail, image).__dict__))

    def __handle_exception(self, type):
        if type == 'format_error':
            return TextSendMessage('The format is incorrect.')


    def __fetch_news(self):
        list = self.__redis.hkeys('temp')
        columns = []
        for index in list:
            news = json.loads(self.__redis.hget('temp', index))
            columns.append(CarouselColumn(
                thumbnail_image_url=news['_News__url'],
                text=news['_News__title'],
                actions=[
                    PostbackTemplateAction(
                        label='Read',
                        data='@Read=' + str(index)
                    ),
                    PostbackTemplateAction(
                        label='Favourite',
                        data='@Favourite=' + str(index)
                    )
                ]
            ))
        message = TemplateSendMessage(
            alt_text='Carousel template',
            template=CarouselTemplate(
                columns=columns
            )
        )
        return message

    # get user list
    def __fetch_list(self):
        favourites = self.__redis.hkeys(self.__userid)
        columns = []
        for index in favourites:
            columns.append(CarouselColumn(
                thumbnail_image_url='https://cdn.i-scmp.com/sites/default/files/styles/1200x800/public/d8/images/methode/2020/03/16/b35ac034-66b4-11ea-8e9f-2d196083a37c_image_hires_082451.jpg?itok=M3BZXPyr&v=1584318299',
                title=str(index),
                text='test',
                actions=[
                    PostbackTemplateAction(
                        label='Delete',
                        data='@Delete=' + str(index)
                    )
                ]
            ))
        message = TemplateSendMessage(
            alt_text='Carousel template',
            template=CarouselTemplate(
                columns=columns
            )
        )
        return message

    # find news by id
    def __read_news(self, index):
        print('=====================================================')
        print(index)
        news = json.loads(self.__redis.hget('temp', index))
        return news['_News__content']

    # delete news by id
    def __delete_favourite(self, index):
        redis = self.__redis
        flag = redis.hdel(self.__userid, index)
        return flag

    def __favourite_news(self, index):
        redis = self.__redis
        news = News('Title1', 'Content1', 'Url1')
        flag = redis.hset(self.__userid, index, json.dumps(news.__dict__))
        return flag

    # handle different type message
    def handle_message(self, index):
        if self.__message == '@News':
            return self.__fetch_news()
        elif self.__message == '@Read':
            return self.__read_news(index)
        elif self.__message == '@Ranking':
            return "developing Ranking"
        elif self.__message == '@Favourite':
            # handel exception 0
            if self.__favourite_news(index) == 1:
                return 'Saved Successfully'
        elif self.__message == '@List':
            return self.__fetch_list()
        elif self.__message == '@Delete':
            # handel exception 0
            if self.__delete_favourite(index) == 1:
                return 'Delete Successfully'
        else:
            return self.__handle_exception('format_error')
