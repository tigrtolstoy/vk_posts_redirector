import os
import sys
import unittest
from dotenv import dotenv_values

root = os.path.join(os.getcwd(), os.path.pardir)
sys.path.append(root)

from src.vk import PostsGetter


config = dotenv_values()

if not len(config):
    raise EnvironmentError('config .env file is empty or does not exists')

vk_token = config['VK_ACCESS_TOKEN']


class TestVkPostsGetter(unittest.TestCase):
    posts_getter = PostsGetter(vk_token)
        
    def test_get_posts_data_types(self):
        with self.assertRaises(TypeError):
            self.posts_getter.get_posts_data(11)

        with self.assertRaises(TypeError):
            self.posts_getter.get_posts_data('11', 'a')

        with self.assertRaises(TypeError):
            self.posts_getter.get_posts_data('11', 1, None)
    
    def test_get_posts_data_values(self):
        with self.assertRaises(AssertionError):
            self.posts_getter.get_posts_data('11')

        with self.assertRaises(AssertionError):
            self.posts_getter.get_posts_data('-11', -1)

        with self.assertRaises(AssertionError):
            self.posts_getter.get_posts_data('11', 1000)

        with self.assertRaises(AssertionError):
            self.posts_getter.get_posts_data('11', 10, -1)
    
    def test_get_posts_data_response(self):
        bad_group_id = '-12341234123421341234213412342134'
        with self.assertRaises(Exception):
            self.posts_getter.get_posts_data(bad_group_id)

    def test_get_posts_data_posts_data(self):
        self.assertIsInstance(self.posts_getter.get_posts_data('-1000324'), list)