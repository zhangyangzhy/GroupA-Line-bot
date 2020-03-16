from WPC.NewsConnection import NewsConnection


class NewsProvider:
    def __init__(self, userid, message):
        self.__redis = NewsConnection.connect()
        self.__userid = userid
        self.__message = message

    # get the latest news
    def getNews(self):
        return self.__message+''+self.__userid
