import json
from time import sleep
from pprint import pprint
from dotenv import dotenv_values

from src.telegram import PostSender
from src.vk import PostsGetter, PostsHandler


if __name__ == '__main__':
    last_sended_post_id = -1
    posts_count = 1
    offset = 10
    timeout = 3


    config_fname = 'groups_ids.json'
    with open(config_fname, 'r') as config_file:
        config = json.load(config_file)

    groups_ids = config['groups_ids']

    env = dotenv_values()

    vk_access_token = env['VK_ACCESS_TOKEN']
    tg_bot_token = env['TG_ACCESS_TOKEN']
    tg_chanel_id = env['TG_CHANEL_ID']

    while True:
        posts_getter = PostsGetter(vk_access_token)
        posts_handler = PostsHandler()
        post_sender = PostSender(tg_bot_token)


        for group_id in groups_ids:
            posts_data = posts_getter.get_posts_data(group_id, count=posts_count, offset=offset)
            group_name = posts_getter.get_group_name(group_id)
            posts = posts_handler.process_posts_data(posts_data, group_name)
            for post in posts:
                if post.id > last_sended_post_id:
                    msg = post.post_to_msg()       
                    post_sender.send_message(msg, tg_chanel_id)
                    last_sended_post_id = post.id
                    if offset > 0:
                        offset -= 1
                    sleep(timeout)

        