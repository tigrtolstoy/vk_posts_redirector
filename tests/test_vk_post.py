import os
import sys

root = os.path.join(os.getcwd(), os.path.pardir)
sys.path.append(root)

import unittest
from datetime import datetime

from src.vk import Post


class TestPost(unittest.TestCase):
    def test_init(self):
        with self.assertRaises(AssertionError):
            _ = Post('a', 'asdf', datetime.now(), 'aaa')

        with self.assertRaises(AssertionError):
            _ = Post(-1, 'asdf', datetime.now(), 'aaa')

        with self.assertRaises(AssertionError):
            _ = Post(0, 11, datetime.now(), 'aaa')

        with self.assertRaises(AssertionError):
            _ = Post(0, 'asdf', 'asdf', 'aaa')

        with self.assertRaises(AssertionError):
            _ = Post(0, 'asdf', datetime.now(), 11)
