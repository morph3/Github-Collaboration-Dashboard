
import sys
import os
import unittest
sys.path.append(os.getcwd() + '/../../src/')

from Utils import *

class TestUtils(unittest.TestCase):

    def test_dot_env(self):
        with open("../../.env", "r") as f:
            token = f.read().split("=")[1].strip()
        self.assertTrue(token.startswith("ghp"))

    # case to check calculation of gini index is correct
    def test_gini_index(self):
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        result = calculate_gini_index(data)
        self.assertEqual(result, 0.2999999994545455)

    # case to check array of every value being same, so gini index should be 0
    def test_gini_index_2(self):
        data = [1, 1, 1, 1, 1]
        result = calculate_gini_index(data)
        self.assertEqual(result, 0.0)

    # case to check array of size is 1, so gini index should be 0
    def test_gini_index3(self):
        data = [2]
        result = calculate_gini_index(data)
        self.assertEqual(result, 0)

if __name__ == '__main__':
    unittest.main(verbosity=4)
