from NewsConnection import NewsConnection


class NewsProvider:
    def __init__(self):
        self.__redis = NewsConnection.connect()

    # get the latest news
    def getNews(self):
        return 'hi'
