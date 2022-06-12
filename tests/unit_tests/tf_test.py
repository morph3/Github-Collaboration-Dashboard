import sys
import os
sys.path.append(os.getcwd() + '/src/')
from TruckFactor import *
from GithubAPIWrapper import *
import unittest




class TestTruckFactor(unittest.TestCase):

# test case to check the heuristic based of the truck factor is correct
    
    def test_heuristic_based_tf(self):
        # initialize the required variables for the test case
        with open(os.getcwd()+"/.env", "r") as f:
            token = f.read().split("=")[1].strip()
        gaw = GithubAPIWrapper(token)
        tfc = TruckFactorCalculator(gaw)
        
        # run the method to get the heuristic based truck factor
        result = tfc.heuristic_based_truck_factor("projectdiscovery/httpx")
        
        
        # test case is true when the user is in the list of users
        self.assertTrue("forgedhallpass" in result["users"])


# test case to check the commit based of the truck factor is correct
    
    def test_commit_based_tf(self):
        # initialize the required variables for the test case
        with open(os.getcwd()+"/.env", "r") as f:
            token = f.read().split("=")[1].strip()
        gaw = GithubAPIWrapper(token)
        tfc = TruckFactorCalculator(gaw)
        
        # run the method to get the commit based truck factor
        result = tfc.commit_based_truck_factor("projectdiscovery/httpx")
        
        
        #test case is true when the user is in the list of users
        self.assertTrue("Sami" in result["users"])

# test case to check the stack based of the truck factor is correct
    
    def test_stack_based_tf(self):
        # initialize the required variables for the test case
        with open(os.getcwd()+"/.env", "r") as f:
            token = f.read().split("=")[1].strip()
        gaw = GithubAPIWrapper(token)
        tfc = TruckFactorCalculator(gaw)
        
        # run the method to get the stack based truck factor
        result = tfc.stack_based_truck_factor("projectdiscovery/httpx")
        
        
        #test case is true when the user is in the list of users
        self.assertTrue("mzack" in result["users"])


if __name__ == "__main__":

    unittest.main()


    # before optimization
    """
    Calculating commit based truck factor for repository: morph3/crawpy
    Time taken to get file list: 0.9751341342926025
    Time taken to get file commits: 4.742347002029419
    Truck Factor: ['morph3'], length: 1
    Time taken to calculate repo 'morph3/crawpy': 5.717698097229004
    Calculating commit based truck factor for repository: xct/ropstar
    Time taken to get file list: 1.0656909942626953
    Time taken to get file commits: 4.419976234436035
    Truck Factor: ['xct'], length: 1
    Time taken to calculate repo 'xct/ropstar': 5.485821962356567
    Calculating commit based truck factor for repository: apexcharts/apexcharts.js
    Time taken to get file list: 1.2761950492858887
    Time taken to get file commits: 434.47521209716797
    Truck Factor: ['Brian Lagunas'], length: 1
    Time taken to calculate repo 'apexcharts/apexcharts.js': 435.75945115089417
    """

    # after optimization
    """
    Calculating commit based truck factor for repository: morph3/crawpy
    Time taken to get file list: 0.9920079708099365
    Time taken to get file commits: 0.5536158084869385
    Truck Factor: ['morph3'], length: 1
    Time taken to calculate repo 'morph3/crawpy': 1.5458149909973145
    Calculating commit based truck factor for repository: xct/ropstar
    Time taken to get file list: 0.9426538944244385
    Time taken to get file commits: 0.5259950160980225
    Truck Factor: ['morph3'], length: 1
    Time taken to calculate repo 'xct/ropstar': 1.4688830375671387
    Calculating commit based truck factor for repository: apexcharts/apexcharts.js
    Time taken to get file list: 1.1818740367889404
    Time taken to get file commits: 14.731389284133911
    Truck Factor: ['Brian Lagunas'], length: 1
    Time taken to calculate repo 'apexcharts/apexcharts.js': 15.92166018486023
    Calculating commit based truck factor for repository: SerenityOS/serenity
    Time taken to get file list: 1.8149068355560303
    Time taken to get file commits: 130.97280406951904
    Truck Factor: ['Andreas Kling'], length: 1
    Time taken to calculate repo 'SerenityOS/serenity': 132.82838082313538
    """
