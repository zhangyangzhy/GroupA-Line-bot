from WPC.NewsConnection import NewsConnection


class NewsProvider:
    def __init__(self, userid, message):
        self.__redis = NewsConnection().connect()
        self.__userid = userid
        self.__message = message

    def __handle_exception(self,type):
        if type=='format_error':
            return 'The format is incorrect.'


    # handle different type message
    def handle_message(self):
        if self.__message=='@News':
            return "developing News"
        elif self.__message:
            return "developing Read"
        elif self.__message:
            return "developing Ranking"
        elif self.__message:
            return "developing Favourite"
        elif self.__message:
            return "developing Delete"
        elif self.__message=='@List':
            return 'developing list'
        else:
            return self.__handle_exception('format_error')




