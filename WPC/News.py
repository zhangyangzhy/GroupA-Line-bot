class News:
    def __init__(self, title, content, url):
        self.__title = title
        self.__content = content
        self.__url = url

    def get_url(self):
        return self.__url

    def get_content(self):
        return self.__content

    def get_title(self):
        return self.__title



