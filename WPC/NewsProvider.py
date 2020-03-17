from urllib import parse

from linebot.models import CarouselColumn, PostbackTemplateAction, TemplateSendMessage, CarouselTemplate

from WPC.News import News
from WPC.NewsConnection import NewsConnection
import re


class NewsProvider:
    def __init__(self, userid, message):
        self.__redis = NewsConnection().connect()
        self.__userid = userid
        self.__message = message
        self.__news_list = []
        self.__news_list.append(News(
            '''Coronavirus: Hong Kong issues ‘red’ travel alert on the United States, Britain and Ireland and imposes quarantine measures on arrivals from the three countries and Egypt''',
            '''Hong Kong has issued a red travel alert on the United States, Britain and Ireland and will impose a 14-day quarantine period on all arrivals from the three countries and Egypt from Thursday in a bid to halt the number of imported Covid-19 infections.
Compulsory home quarantine would apply to everyone, including Hong Kong residents, arriving in the city from March 19 who had been to any of the four countries in the previous 14 days, the government announced on Sunday night.
The red alert is the second level of a three-tier system and warns of a “significant threat” at the destination involved.''',
            'https://cdn.i-scmp.com/sites/default/files/styles/1200x800/public/d8/images/methode/2020/03/16/b35ac034-66b4-11ea-8e9f-2d196083a37c_image_hires_082451.jpg?itok=M3BZXPyr&v=1584318299'))
        self.__news_list.append(
            News('''Coronavirus: China vows to help Spain amid questions over EU support for its worst-hit countries''',
                 '''China has widened its coronavirus diplomacy in Europe, with Foreign Minister Wang Yi pledging medical support for Spain, which begins a national lockdown on Monday.
Italy, the outbreak’s worst-hit country after China, also said on Sunday it would receive from China 5 million masks, 150 ventilators and two extra medical teams.
Chinese medical assistance for Europe’s two most severely affected nations came as Italy accused European Union members of failing to send the equipment needed.
China’s actions also coincided with the United States’ tensions with Europe. The White House has issued a travel ban for the whole of Europe, while it is also, according to the German ministry of health, trying to acquire a German pharmaceutical company specialising in Covid-19 vaccine developments.''',
                 'https://cdn.i-scmp.com/sites/default/files/styles/1200x800/public/d8/images/methode/2020/03/16/f8da272a-672d-11ea-9de8-4adc9756b5c3_image_hires_150435.jpg?itok=FBxFYBHO&v=1584342281'))
        self.__news_list.append(News(
            '''New monthly low for Hong Kong’s battered tourism sector with arrivals plunging to 199,000 – daily average for early 2019''',
            '''Hong Kong’s battered tourism sector hit a new low amid the coronavirus epidemic in February when arrivals slumped to 199,000 – the daily average in the first half of last year.
The Tourism Board’s latest statistics showed a drop of more than 96 per cent year-on-year for the period, after the government rolled out measures from February 8 to stem the spread of Covid-19 by closing all but three border checkpoints with mainland China.
For the rest of that month, the average number of tourists coming to the city per day stood at just 3,300, of which only one in five were mainland Chinese, who used to account for about 80 per cent of all Hong Kong’s visitors.
Across the globe, 47 countries and jurisdictions issued advisories against travel to mainland China, with 28 of those including Hong Kong.''',
            'https://cdn.i-scmp.com/sites/default/files/styles/1200x800/public/d8/images/methode/2020/03/16/859fdc2c-6670-11ea-8e9f-2d196083a37c_image_hires_092715.JPG'))

    def __handle_exception(self, type):
        if type == 'format_error':
            return 'The format is incorrect.'

    def __fetch__news(self):
        columns = []
        for index, new in enumerate(self.__news_list):
            columns.append(CarouselColumn(
                thumbnail_image_url=new.get_url(),
                title=new.get_title()[0:25],
                text=new.get_content()[0:35] + '...',
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

    # find news by id
    def __find_news(self, index):
        return self.__news_list[index]

    # handle different type message
    def handle_message(self, index):
        if self.__message == '@News':
            return self.__fetch__news()
        elif self.__message == '@Read':
            return self.__news_list[index]
        elif self.__message == '@Ranking':
            return "developing Ranking"
        elif self.__message:
            if re.match('@Favourite \d+$', self.__message) is not None:
                return "developing Favourite"
            else:
                return self.__handle_exception('format_error')
        elif self.__message:
            if re.match('@Delete \d+$', self.__message) is not None:
                return "developing Delete"
            else:
                return self.__handle_exception('format_error')
        elif self.__message == '@List':
            return 'developing list'
        else:
            return self.__handle_exception('format_error')
