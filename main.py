import json
from pprint import pprint
from dotenv import dotenv_values

from src.vk import PostsGetter, PostsHandler


config_fname = 'groups_ids.json'
with open(config_fname, 'r') as config_file:
    config = json.load(config_file)

groups_ids = config['groups_ids']

env = dotenv_values()

vk_access_token = env['VK_ACCESS_TOKEN']

posts_getter = PostsGetter(vk_access_token)
posts_handler = PostsHandler()


for group_id in groups_ids:
    posts_data = posts_getter.get_posts_data(group_id, count=10)
    group_name = posts_getter.get_group_name(group_id)
    posts = posts_handler.process_posts_data(posts_data, group_name)
    for post in posts:
        print(post)
        print()
        print()
        print()
