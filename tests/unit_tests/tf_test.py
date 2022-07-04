import sys
import os
sys.path.append(os.getcwd() + '/src/')
sys.path.append(os.getcwd() + '/../../src/')

from TruckFactor import *
from GithubAPIWrapper import *
import unittest

# load token
token = ""
try:
    with open(os.getcwd()+"/.env", "r") as f:
        token = f.read().split("=")[1].strip()
except:
    with open(os.getcwd()+"/../../.env", "r") as f:
        token = f.read().split("=")[1].strip()

# initialize the required variables for the test case
gaw = GithubAPIWrapper(token)
tfc = TruckFactorCalculator(gaw)

class TestTruckFactor(unittest.TestCase):

    # test case to check the heuristic based of the truck factor is correct
    def test_heuristic_based_tf(self):
        
        # run the method to get the heuristic based truck factor
        result = tfc.heuristic_based_truck_factor("projectdiscovery/httpx")
        
        
        # test case is true when the user is in the list of users
        self.assertTrue("forgedhallpass" in result["users"])


    # test case to check the commit based of the truck factor is correct
    def test_commit_based_tf(self):

        # run the method to get the commit based truck factor
        result = tfc.commit_based_truck_factor("projectdiscovery/httpx")
        
        
        #test case is true when the user is in the list of users
        self.assertTrue("Sami" in result["users"])

    # test case to check the stack based of the truck factor is correct
    def test_stack_based_tf(self):

        # run the method to get the stack based truck factor
        result = tfc.stack_based_truck_factor("projectdiscovery/httpx")
        
        
        #test case is true when the user is in the list of users
        self.assertTrue("mzack" in result["users"])


if __name__ == "__main__":

    unittest.main(verbosity=2)
