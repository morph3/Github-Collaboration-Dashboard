import unittest
import sys
import os
sys.path.append(os.getcwd() + '/../src/')

from Utils import *

"""
TODO: convert them into unit tests
"""
class TestUtils(unittest.TestCase):

    def test_dot_env(self):
        with open("../.env", "r") as f:
            token = f.read().split("=")[1].strip()
        self.assertTrue(token.startswith("ghp"))

if __name__ == '__main__':
    unittest.main()
    """
    TODO: convert below into unit tests
    "For test purposes"

    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print(calculate_gini_index(data))
    data = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    print(calculate_gini_index(data))
    data=[1]
    print(calculate_gini_index(data))

    """
