import unittest
import sys
import os
sys.path.append(os.getcwd() + '/../src/')

from TruckFactor import *
from GithubAPIWrapper import *


class TestTruckFactor(unittest.TestCase):
    def test_heuristic_based_tf(self):
        with open("../.env", "r") as f:
            token = f.read().split("=")[1].strip()
        gaw = GithubAPIWrapper(token)
        tfc = TruckFactorCalculator(gaw)
        result = tfc.heuristic_based_truck_factor("projectdiscovery/httpx")
        #print(result)
        self.assertTrue("Ice3man" in result["users"])
    
    def another_test(self):
        pass

if __name__ == "__main__":

    unittest.main()
    
    
    """
    TODO: convert those below into unittests


    token = open("../.env","r").read().split("=")[1].strip()
    gaw = GithubAPIWrapper(token)


    tfc = TruckFactorCalculator(gaw)

    start_time = time.time()
    tfc.stack_based_truck_factor("morph3/crawpy")
    end_time = time.time()
    print(f"Time taken to calculate repo 'morph3/crawpy': {end_time - start_time}")

    start_time = time.time()
    tf.commit_based_truck_factor("SerenityOS/serenity")
    end_time = time.time()
    print(f"Time taken to calculate repo 'SerenityOS/serenity': {end_time - start_time}")



    start_time = time.time()
    tf.commit_based_truck_factor("xct/ropstar")
    end_time = time.time()
    print(f"Time taken to calculate repo 'xct/ropstar': {end_time - start_time}")


    start_time = time.time()
    tf.commit_based_truck_factor("apexcharts/apexcharts.js")
    end_time = time.time()
    print(f"Time taken to calculate repo 'apexcharts/apexcharts.js': {end_time - start_time}")


    start_time = time.time()
    tf.commit_based_truck_factor("SerenityOS/serenity")
    end_time = time.time()
    print(f"Time taken to calculate repo 'SerenityOS/serenity': {end_time - start_time}")

    """


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
