from WPC.NewsConnection import NewsConnection


class NewsProvider:
    def __init__(self, userid, message):
        self.__redis = NewsConnection().connect()
        self.__userid = userid
        self.__message = message

    # handle different type message
    def handle_message(self):


