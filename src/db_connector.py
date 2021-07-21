import sqlite3


class DBConnector:
    def __init__(self, path_to_db_file):
        self.__connection = sqlite3.connect(path_to_db_file)
        create_table_query = '''
            CREATE TABLE IF NOT EXISTS public_sended_post (
            public_id INT PRIMARY KEY,
            last_sended_post_id INT
        )
        '''
        self.__connection.execute(create_table_query)
    
    def get_last_sended_post_id(self, group_id):
        query = f'SELECT last_sended_post_id FROM public_sended_post WHERE public_id = {group_id}'
        cursor = self.__connection.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        if result is not None:
            return result[0]
        return result

    def update_last_sended_post(self, group_id, post_id):
        query = \
            f'INSERT OR REPLACE INTO public_sended_post (public_id, last_sended_post_id) values ({group_id}, {post_id})'
        cursor = self.__connection.cursor()
        cursor.execute(query)
        cursor.close()
        self.commit()

    def commit(self):
        self.__connection.commit()

    def close(self):
        self.__connection.close()
