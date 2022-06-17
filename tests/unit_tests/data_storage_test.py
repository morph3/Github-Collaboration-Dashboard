import unittest
import sys
import os
sys.path.append(os.getcwd() + '/src/')
sys.path.append(os.getcwd() + '/../../src/')

from DataStorage import *

storage = SimpleStorage()
try:
    storage.load_file(os.getcwd() + "/storage.json")
except:
    storage.load_file(os.getcwd() + "/../../storage.json")

class TestDataStorage(unittest.TestCase):

# test cases to check the method is adding data to the storage
    def test_load_file(self):
        # test is true when the storage.json file exists and it is loaded correctly
        self.assertEqual( storage.storage[0]["repository_name"] , "HashLips/hashlips_art_engine") 
    
# test cases to check the method is getting the element of the storage based on the given info    
    def test_get_all(self):
        # you can change the expected result to test the method
        expected_result = [{'repository_name': 'HashLips/hashlips_art_engine', 'type': 'heuristic', 'users': [
                            'hashlips', 'Ben Halverson', 'HashLips', 'Daniel Botha'], 'truck_factor': 4, 
                            'date': '2022-01-20 00:33:38'}]
        
        # run the method 
        test_result = storage.get_all("HashLips/hashlips_art_engine", "heuristic")
        
        # test is true when the expected result is equal to the test result
        self.assertEqual( test_result, expected_result)

# test cases to check the method is getting the last element of the storage based on the given info
    def test_get_last(self):
        
        # you can change the expected result to test the method
        expected_result = {
            "repository_name": "projectdiscovery/httputil",
            "type": "stack",
            "users": [
                "mzack",
                "Mzack9999"
            ],
            "truck_factor": 2,
            "date": "2022-06-13 15:54:33"
        }
        
        # run the method
        test_result = storage.get_last("projectdiscovery/httputil", "stack")
        
        # test is true when the expected result is equal to the test result
        self.assertEqual(test_result, expected_result)





if __name__ == "__main__":
    unittest.main(verbosity=2)

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
