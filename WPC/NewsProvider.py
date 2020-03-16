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
The red alert is the second level of a three-tier system and warns of a “significant threat” at the destination involved.'''))
        self.__news_list.append(
            News('''Coronavirus: China vows to help Spain amid questions over EU support for its worst-hit countries''',
                 '''China has widened its coronavirus diplomacy in Europe, with Foreign Minister Wang Yi pledging medical support for Spain, which begins a national lockdown on Monday.
Italy, the outbreak’s worst-hit country after China, also said on Sunday it would receive from China 5 million masks, 150 ventilators and two extra medical teams.
Chinese medical assistance for Europe’s two most severely affected nations came as Italy accused European Union members of failing to send the equipment needed.
China’s actions also coincided with the United States’ tensions with Europe. The White House has issued a travel ban for the whole of Europe, while it is also, according to the German ministry of health, trying to acquire a German pharmaceutical company specialising in Covid-19 vaccine developments.'''))
        self.__news_list.append(News(
            '''New monthly low for Hong Kong’s battered tourism sector with arrivals plunging to 199,000 – daily average for early 2019''',
            '''Hong Kong’s battered tourism sector hit a new low amid the coronavirus epidemic in February when arrivals slumped to 199,000 – the daily average in the first half of last year.
The Tourism Board’s latest statistics showed a drop of more than 96 per cent year-on-year for the period, after the government rolled out measures from February 8 to stem the spread of Covid-19 by closing all but three border checkpoints with mainland China.
For the rest of that month, the average number of tourists coming to the city per day stood at just 3,300, of which only one in five were mainland Chinese, who used to account for about 80 per cent of all Hong Kong’s visitors.
Across the globe, 47 countries and jurisdictions issued advisories against travel to mainland China, with 28 of those including Hong Kong.'''))

    def __handle_exception(self, type):
        if type == 'format_error':
            return 'The format is incorrect.'

    def __fetch__news(self):
        title = [
            '''Coronavirus: Hong Kong issues ‘red’ travel alert on the United States, Britain and Ireland and imposes quarantine measures on arrivals from the three countries and Egypt''',
            '''Coronavirus: China vows to help Spain amid questions over EU support for its worst-hit countries''',
            '''New monthly low for Hong Kong’s battered tourism sector with arrivals plunging to 199,000 – daily average for early 2019''']
        titles = ''
        for i in range(3):
            titles += str(i + 1) + '. '
            titles += title[i]
            titles += '\n\n\n'
        return titles

    # handle different type message
    def handle_message(self):
        if self.__message == '@News':
            return self.__fetch__news()
        elif self.__message:
            if re.match('@Read \d+$', self.__message) is not None:
                return 'developing Read'
            else:
                return self.__handle_exception('format_error')
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
