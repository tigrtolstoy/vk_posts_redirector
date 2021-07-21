import requests


class PostsGetter:
    '''
      Класс для получения постов из группы ВК
    '''
    __API_VERSION = 5.131

    def __init__(self, api_token):
        self.__api_token = api_token

    def get_posts_data(self, group_id, count=10, offset=0):
        # Получаем count постов начиная с offset
        method = 'wall.get'
        query_params = self.__create_query_params_string(group_id, count, offset)
        query = self.__create_query(method, query_params)
        response = requests.get(query)
        response_data = self.__process_response(response)
        posts_data = self.__get_posts_from_response_data(response_data)
        return posts_data
    
    def get_group_name(self, group_id):
        # Получаем имя группы по id
        method = 'groups.getById'
        query_params = f'group_id={group_id[1:]}'
        query = self.__create_query(method, query_params)
        response = requests.get(query)
        response_data = self.__process_response(response)
        try:
            group_name = response_data['response'][0]['name']
            return group_name
        except KeyError as e:
            raise Exception(
                f'Bad response: \n{response_data}') from e
    
    @staticmethod
    def __process_response(response):
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise Exception('Bad response status') from e

        response_data = response.json()
        return response_data
        

    @staticmethod
    def __get_posts_from_response_data(response_data):
        try:
            posts_data = response_data['response']['items']
            return posts_data
        except KeyError as e:
            raise Exception(
                f'Bad response: \n{response_data}') from e
    
    def __create_query(self, method, query_params):
        base_query = \
            'https://api.vk.com/method/{}?{}&access_token={}&v={}'
        query = base_query.format(method,
                                  query_params,
                                  self.__api_token,
                                  self.__API_VERSION)
        return query

    @staticmethod
    def __create_query_params_string(group_id, count, offset):
        if not isinstance(group_id, str):
            raise TypeError()
        if not isinstance(count, int):
            raise TypeError()
        if not isinstance(offset, int):
            raise TypeError()
            
        assert group_id[0] == '-', 'group id must start with "-"'
        assert 0 <= count <= 100, 'count must be between 0 and 100'
        assert offset >= 0, 'offset must be greater'

        group_id_str = f'owner_id={group_id}'
        count_str = f'count={count}'
        offset_str = f'offset={offset}'
        return '&'.join([group_id_str, count_str, offset_str])
