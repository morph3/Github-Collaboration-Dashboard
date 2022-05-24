import unittest
import sys
import os
sys.path.append(os.getcwd() + '/../../src/')

from DataStorage import *

class TestDataStorage(unittest.TestCase):

    def test_load_file(self):
        storage = SimpleStorage()
        storage.load_file("../../storage.json")
        self.assertEqual( storage.storage[0]["repository_name"] , "HashLips/hashlips_art_engine") 
        
    def test_get_all(self):
        pass


if __name__ == "__main__":
    unittest.main()

    """
    repo_name = "projectdiscovery/httpx"
    type      = "heuristic"

    print(f"All items for '{repo_name}': {storage.get_all('projectdiscovery/httpx','heuristic')}")

    last_item = storage.get_last('projectdiscovery/httpx','heuristic')
    #print(last_item)
    if last_item:
        print(f"Last item for '{repo_name}': {last_item}")

    """
    # TODO:
    # Add more tests here.
