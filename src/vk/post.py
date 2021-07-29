from datetime import datetime


class Post:
    '''
      Класс реализует структуру данных для постов ВК
    '''
    def __init__(self, post_id, url, public_name, date, text, is_pinned):
        assert isinstance(post_id, int), 'post id must be int'
        assert post_id >= 0, 'post id must be greater the 0'
        assert isinstance(url, str), 'post url must be str'
        assert isinstance(public_name, str), 'public name must be str'
        assert isinstance(date, datetime), 'post date must be datetime'
        assert isinstance(text, str), 'post text must be str'
        assert isinstance(is_pinned, bool), 'is_pinned satus must be str'

        self.__id = post_id
        self.__url = url
        self.__public_name = public_name
        self.__date = date
        self.__text = text
        self.__is_pinned = is_pinned
    
    @property
    def id(self):
        return self.__id

    @property 
    def url(self):
        return self.__url
    
    @property
    def public_name(self):
        return self.__public_name
    
    @property
    def date(self):
        return self.__date
    
    @property
    def text(self):
        return self.__text
    
    @property
    def is_pinned(self):
        return self.__is_pinned

    def to_msg(self):
        # Конветирует информацию в строку
        # Может использоваться для отправки сообщения
        id_str = f'id: {self.__id}'
        url_str = f'url: {self.__url}'
        public_str = f'{self.__public_name}'

        text_sep = '='*50
        text_str = f'{text_sep}\n{self.__text}\n{text_sep}'

        str_date = self.__date_to_string(self.__date)

        msg = f'{str_date}\n<a href="{url_str}">ссылка на пост</a>\n\n<b>{public_str}</b>\n\n\n{self.__text}'
        
        return msg
    
    def __repr__(self):
        return self.to_msg()

    @staticmethod
    def __date_to_string(date):
        str_date = date.strftime('%d/%m/%Y %H:%M')
        return str_date
