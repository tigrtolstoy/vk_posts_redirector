import json
import atexit
from time import sleep
from dotenv import dotenv_values
from requests.exceptions import ConnectionError

from src.db_connector import DBConnector

from src.telegram import PostSender
from src.vk import PostsGetter, PostsHandler
from src.posts_collector import PostsCollector


SENDING_TIMEOUT = 3

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
def safely_close_db():
    db_connector.commit()
    db_connector.close()


posts_collectors = []
for group_id in groups_ids:
    collector = PostsCollector(vk_access_token, group_id)
    posts_collectors.append(collector)


def collect_posts(collector, last_sended_post):
    collector.collect_posts_to_send(
        posts_getter,
        posts_handler,
        last_sended_post
    )


def send_collected_posts(collector, last_sended_post):
    while collector.is_posts_to_send():
        post = collector.get_post_to_send()
        msg = post.to_msg()
        post_sender.send_message(msg, tg_chanel_id)
        if last_sended_post is None or post.id > last_sended_post:
            db_connector.update_last_sended_post(
                collector.target_group_id,
                post.id
            )
        collector.pop_last_post()
        sleep(SENDING_TIMEOUT)


if __name__ == '__main__':
    while True:
        for collector in posts_collectors:
            try:
                last_sended_post = db_connector.get_last_sended_post_id(
                    collector.target_group_id
                )
                collect_posts(collector, last_sended_post)
                send_collected_posts(collector, last_sended_post)
            except ConnectionError as e:
                sleep(5) # waiting for internet
