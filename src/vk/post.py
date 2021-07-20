from datetime import datetime


class Post:
    def __init__(self, post_id, url, date, text):
        assert isinstance(post_id, int), 'post id must be int'
        assert post_id >= 0, 'post id must be greater the 0'
        assert isinstance(url, str), 'post url must be str'
        assert isinstance(date, datetime), 'post date must be datetime'
        assert isinstance(text, str), 'post text must be str'

        self.__id = post_id
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

    def __repr__(self):
        id_str = f'id: {self.__id}'
        url_str = f'url: {self.__url}'

        text_sep = '='*50
        text_str = f'{text_sep}\n{self.__text}\n{text_sep}'

        str_date = self.__date_to_string(self.__date)
        date_str = f'date: {str_date}'
        return '\n'.join([id_str, url_str, date_str, text_str])

    @staticmethod
    def __date_to_string(date):
        str_date = date.strftime('%d/%m/%Y %H:%M')
        return str_date