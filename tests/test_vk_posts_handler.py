import unittest
from src.vk import PostsHandler


class TestPostHandler(unittest.TestCase):
    ph = PostsHandler()
    
    def test_processing_of_post(self):
        
        with self.assertRaises(AssertionError):
            self.ph.process_posts_data('a')

        with self.assertRaises(Exception):
            post = {
                'owner_id': '-34343',
                'date': '123551'
            }
            self.ph.process_posts_data([post])

        with self.assertRaises(Exception):
            post = {
                'id': '11',
                'date': '123551'
            }
            self.ph.process_posts_data([post])

        with self.assertRaises(Exception):
            post = {
                'id': '11',
                'owner_id': '-34343'
            }
            self.ph.process_posts_data([post])
        
    def test_empty_text(self):
        post = {
            'id': '11',
            'owner_id': '-34343',
            'date': 112312
        }
        posts = self.ph.process_posts_data([post])
        processed_post = posts[0]
        self.assertEqual(processed_post.text, '')

        
    def test_str_timestemp(self):
        post = {
            'id': '11',
            'owner_id': '-34343',
            'date': '112312'
        }
        with self.assertRaises(AssertionError):
            _ = self.ph.process_posts_data([post])