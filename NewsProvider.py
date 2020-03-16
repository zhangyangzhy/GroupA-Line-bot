from NewsConnection import NewsConnection


class NewsProvider:
    def __init__(self, userid):
        self.__redis = NewsConnection.connect()
        self.__userid = userid

    # get the latest news
    def getNews(self):
        return self.__userid

