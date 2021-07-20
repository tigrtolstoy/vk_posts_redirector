import json
import atexit
from time import sleep
from dotenv import dotenv_values

from src.db_connector import DBConnector
from src.telegram import PostSender
from src.vk import PostsGetter, PostsHandler


if __name__ == '__main__':
    last_sended_post_id = -1
    posts_count = 50 
    offset = 1000
    timeout = 3


    config_fname = 'groups_ids.json'
    with open(config_fname, 'r') as config_file:
        config = json.load(config_file)

    groups_ids = config['groups_ids']

    env = dotenv_values()

    vk_access_token = env['VK_ACCESS_TOKEN']
    tg_bot_token = env['TG_ACCESS_TOKEN']
    tg_chanel_id = env['TG_CHANEL_ID']
    path_to_db = 'db/publics.db'

    posts_getter = PostsGetter(vk_access_token)
    posts_handler = PostsHandler()
    post_sender = PostSender(tg_bot_token)
    db_connector = DBConnector(path_to_db)

    @atexit.register
    def close_db():
        db_connector.commit()
        db_connector.close()

    while True:
        for group_id in groups_ids:
            
            posts_data = posts_getter.get_posts_data(group_id, count=posts_count, offset=offset)
            group_name = posts_getter.get_group_name(group_id)
            posts = posts_handler.process_posts_data(posts_data, group_name)
            for post in posts:
                last_sended_post_id = db_connector.get_last_sended_post_id(int(group_id))
                if last_sended_post_id is None:
                    last_sended_post_id = -1

                if post.id > last_sended_post_id:
                    msg = post.post_to_msg()       
                    post_sender.send_message(msg, tg_chanel_id)

                    db_connector.update_last_sended_post(int(group_id), post.id)                   

                    sleep(timeout)
                else:
                    sleep(1)

                if offset > 0:
                    offset -= posts_count


        