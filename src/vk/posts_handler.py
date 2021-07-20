from datetime import datetime

from src.vk import Post


class PostsHandler:
    def process_posts_data(self, posts_data):
        sorted_posts = self.__sort_posts_by_date(posts_data)
        posts = []
        for post_data in sorted_posts:
            post = self.__process_post_data(post_data)
            posts.append(post)
        return posts
    
    def __process_post_data(self, post_data):
        url = self.__get_post_url(post_data)
        date = self.__get_post_date(post_data)
        text = self.__get_post_text(post_data)
        return Post(url, date, text)

    def __sort_posts_by_date(self, posts):
        sort_key = lambda post: self.__get_post_timestamp(post)
        sorted_posts = sorted(posts, key=sort_key)
        return sorted_posts

    def __get_post_url(self, post):
        post_id = self.__get_post_id(post)
        owner_id = self.__get_post_owner_id(post)
        return f'https://m.vk.com/wall{owner_id}_{post_id}'
    
    def __get_post_id(self, post):
        post_id = self.__get_post_itme(post, 'id')
        return post_id
    
    def __get_post_owner_id(self, post):
        owner_id = self.__get_post_item(post, 'owner_id')
        return owner_id
    
    def __get_post_timestamp(self, post):
        post_timestamp = self.__get_post_item(post, 'date')
        return post_timestamp
        
    def __get_post_date(self, post):
        post_timestamp = self.__get_post_timestamp(post)
        post_date = self.__timestamp_to_date(post_timestamp)
        return post_date
    
    def __get_post_text(self, post):
        text = self.__get_post_item(post, 'text')
        return text

    @staticmethod
    def __get_post_item(post, item_name):
        try:
            post_item = post[item_name]
            return post_item
        except KeyError as e:
            raise Exception(
                f'Cannot find [{item_name}] in post: {post}') from e
            
    @staticmethod
    def __timestamp_to_date(timestamp):
        date = datetime.fromtimestamp(timestamp)
        return date
