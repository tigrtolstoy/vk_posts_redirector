from time import sleep
from datetime import datetime, timedelta

from src.stack import Stack


class PostsCollector:
    '''
    Класс для сбора записей со стены группы ВК
    '''
    __SLEEPING_TIME = 0.5
    def __init__(self, vk_access_token, group_id, posts_counter=5):
        self.__posts_to_send = Stack()

        self.__group_id = group_id
        self.__posts_counter = posts_counter
    
    @property
    def target_group_id(self):
        return self.__group_id
    
    def collect_posts_to_send(self, posts_getter, posts_handler, last_sended_post_id):
        '''
          Собрать записи после определенной (last_sended_post_id - отправленная последней)
          или за последние 3 дня, если еще ни одна запись не была отправлена
        '''
        offset = 0
        count = self.__posts_counter
        group_name = posts_getter.get_group_name(self.__group_id)

        all_posts_collected = False
        while not all_posts_collected:
            if last_sended_post_id is not None: # Если какие-то записи уже были отправлены
                all_posts_collected = self.__collect_posts(posts_getter, 
                                                        posts_handler,
                                                        group_name,
                                                        offset,
                                                        last_sended_post_id)
            else: # Если никаких записей еще не было отправлено
                all_posts_collected = self.__collect_last_days_posts(posts_getter,
                                                                     posts_handler,
                                                                     group_name,
                                                                     offset)
            offset += count
            self.__wait()

    def __collect_posts(self, posts_getter, posts_handler, group_name, offset, last_sended_post_id):
        all_posts_collected = False
        posts_data = posts_getter.get_posts_data(self.__group_id,
                                                 self.__posts_counter,
                                                 offset)    
        posts = posts_handler.process_posts_data(posts_data, group_name)
        for post in posts:
            if post.id > last_sended_post_id:
                self.__posts_to_send.push(post)
            else:
                if not post.is_pinned:
                    all_posts_collected = True
        return all_posts_collected

    def __collect_last_days_posts(self, posts_getter, posts_handler, group_name, offset):
        now = datetime.now()
        dst_date = now - timedelta(days=3)
        all_posts_collected = False
        posts_data = posts_getter.get_posts_data(self.__group_id,
                                                 self.__posts_counter,
                                                 offset)    
        posts = posts_handler.process_posts_data(posts_data, group_name)
        for post in posts:
            if post.date > dst_date:
                self.__posts_to_send.push(post)
            else:
                if not post.is_pinned:
                    all_posts_collected = True
        return all_posts_collected

    def is_posts_to_send(self):
        return not self.__posts_to_send.is_empty

    def get_post_to_send(self):
        return self.__posts_to_send.get()
    
    def pop_last_post(self):
        self.__posts_to_send.pop()

    def __wait(self):
        sleep(self.__SLEEPING_TIME)

