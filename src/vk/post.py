class Post:
    def __init__(self, url, date, text):
        self.__url = url
        self.__date = date
        self.__text = text
    
    @property 
    def url(self):
        return self.__url
    
    @property
    def date(self):
        return self.__date
    
    @property
    def text(self):
        return self.__text
