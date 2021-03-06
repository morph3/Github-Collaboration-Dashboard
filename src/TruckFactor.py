import requests
import operator
import math
try:
    from src.GithubAPIWrapper import GithubAPIWrapper
except:
    from GithubAPIWrapper import GithubAPIWrapper
import time
import json
from datetime import datetime

class TruckFactorCalculator:
    def __init__(self,gaw):
        self.gaw = gaw # GithubAPIWrapper object
        pass

    # Src: A Novel Approach for Estimating Truck Factors - Guilherme Avelino, Leonardo Passos, Andre Hora and Marco Tulio Valente
    def commit_based_truck_factor(self,repository_full_name):
        """
        Calculates the commit based truck factor for a given repository

        :param repository_full_name: The full name of the repository
        :return: a json object that has entries, truck factor result, repository full name, users that form the truck factor and truck factor type,

        Ex:
        {
            "repository-name": "apexcharts/apexcharts.js",
            "type": "commit",
            "users": ["Juned Chhipa", "Sergey", "junedchhipa", "Wojciech Frącz", "morph3", "Nemanja M", "Unknown", "Carl St-Laurent", "Konstantin Dinev", "Forbidden", "Thijs-jan Veldhuizen", "TomohiroHiratsuka", "Zura Jijavadze", "Martin Kravec", "Saleh", "Lea Verou", "yrajabi", "Brian Lagunas"],
            "truck-factor": 18
        }
        """

        # those prints can stay here as they are not leaked to outside
        print(f"Calculating commit based truck factor for repository: {repository_full_name}")
        start_time = time.time()
        file_list = self.gaw.get_files(repository_full_name)
        end_time = time.time()
        print(f"Time taken to get file list: {end_time-start_time}")



        start_time = time.time()
        file_commits = self.gaw.get_file_commits(repository_full_name, file_list)
        end_time = time.time()
        print(f"Time taken to get file commits: {end_time-start_time}")


        file_commits = dict((k, v) for k, v in file_commits.items() if v) # We remove the empty arrays

        changeCount = {} # Number of commits of users
        fileCreator = {} # Creator of each file

        # k is the file name
        # v[i] is the each user that commited
        for k, v in file_commits.items():
            changeCount[k] = {}
            for i in range(0,len(v)):
                try:
                    changeCount[k][v[i]] += 1
                except:
                    changeCount[k][v[i]] = 1
                if i == (len(v) - 1): # Assumed first commited user is creator of file. Because of structure of json it is the last element
                    fileCreator[k] = v[i]

        changeCountExcept = {} # Number of commits except current user
        # k is the file name
        # key and a are the user names
        # b is the number of commits of user
        for k, v in changeCount.items():
            changeCountExcept[k] = {}
            for key in v.keys():
                changeCountExcept[k][key] = 0
                for a, b in v.items():
                    if a != key: # Because of we need other user's commit count. We don't include current user
                        changeCountExcept[k][key] += changeCount[k][a]

        doaValue = {} # Degree Of Author. Formula is from A_novel_approach_for_estimating_Truck_Factors.pdf
        totalDoa = {} # We need total doa of each file to normalize data
        totalFileCount = 0
        for k, v in changeCount.items():
            totalFileCount += 1
            doaValue[k] = {}
            for a, b in v.items():
                if a == fileCreator[k]:
                    fa = 1
                else:
                    fa = 0
                doaValue[k][a] = 3.293 + (1.098 * fa) + (0.164 * changeCount[k][a]) - (0.321 * math.log(1 + changeCountExcept[k][a]))
                # This formula is from pdf
                try:
                    totalDoa[k] = totalDoa[k] + doaValue[k][a]
                except:
                    totalDoa[k] = doaValue[k][a]

        authoredFiles = {}
        for k, v in changeCount.items():
            for a, b in v.items():
                normalizeDoa = doaValue[k][a] / totalDoa[k]
                if normalizeDoa >= 0.75: # This threshold is from pdf. If normalizedDoa is above our threshold then we count the user as author of that file
                    try:
                        authoredFiles[a] += 1
                    except:
                        authoredFiles[a] = 1


        sortedAuthoredFiles = {}
        for x in sorted(authoredFiles.items(), key=lambda a: a[1], reverse=True):
            sortedAuthoredFiles[x[0]] = authoredFiles[x[0]]

        truckFactor = []
        coverage = 0
        for k,v in sortedAuthoredFiles.items():
            truckFactor.append(k)
            coverage += v
            if coverage > (totalFileCount / 2): #If we looked half of the files than we break
                break

        print(f"Truck Factor: {truckFactor}, length: {len(truckFactor)}")
        entry                       = {}
        entry["repository_name"]    = repository_full_name
        entry["type"]               = "commit"
        entry["users"]              = truckFactor
        entry["truck_factor"]       = len(truckFactor)
        entry["date"]               = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return entry

    # Src: Assessing the bus factor of Git repositories - Valerio Cosentino, Javier Cánovas Izquierdo, Jordi Cabot
    def heuristic_based_truck_factor(self,repository_full_name):
        """
        Calculates the heuristic based truck factor for a given repository

        :param repository_full_name: The full name of the repository
        :return: array of users that build the truck factor
        """

        # those prints can stay here as they are not leaked to outside
        print(f"Calculating heuristic based truck factor for repository: {repository_full_name}")
        start_time = time.time()
        file_list = self.gaw.get_files(repository_full_name)
        end_time = time.time()
        print(f"Time taken to get file list: {end_time-start_time}")



        start_time = time.time()
        file_commits = self.gaw.get_file_commits(repository_full_name, file_list)
        end_time = time.time()
        print(f"Time taken to get file commits: {end_time-start_time}")


        file_commits = dict((k, v) for k, v in file_commits.items() if v) # We remove the empty arrays

        changeCount = {} # Number of commits of users

        # k is the file name
        # v[i] is the each user that commited
        for k, v in file_commits.items():
            changeCount[k] = {}
            for i in range(0,len(v)):
                try:
                    changeCount[k][v[i]] += 1
                except:
                    changeCount[k][v[i]] = 1

        totalCommitCount = {} # Total commit count of a file
        knowledgeOfFile = {} # User's knowledge of file is (total commit count of user) / (total commit count of file)
        primaryDeveloper = {}
        secondaryDeveloper = {}
        ownership = {} # Ownership = totalCountOfPrimaryDeveloper + (totalCountOfSecondaryDeveloper)/2
        # k is the file name
        # v[i] is the each user that commited
        totalFileCount = 0
        for k, v in changeCount.items():
            totalFileCount += 1
            totalCommitCount[k] = 0
            primaryDeveloper[k] = []
            secondaryDeveloper[k] = []
            for name, count in v.items():
                totalCommitCount[k] += count
            primaryThreshold = 1 / float(len(v))        # Threshold to be primary developer. 1 / (total user count of file)
            secondaryThreshold = primaryThreshold / 2   # Threshold to be secondary developer
            for name, count in v.items():
                knowledgeOfFile[name] = float(changeCount[k][name]) / float(totalCommitCount[k])
                if knowledgeOfFile[name] >= primaryThreshold:
                    primaryDeveloper[k].append(name)
                    try:
                        ownership[name] += 2
                    except:
                        ownership[name] = 2
                elif knowledgeOfFile[name] >= secondaryThreshold:
                    secondaryDeveloper[k].append(name)
                    try:
                        ownership[name] += 1
                    except:
                        ownership[name] = 1

        totalUserCount = len(ownership)
        print("Number of people: " + str(totalUserCount))
        truckFactorThreshold = totalFileCount / totalUserCount   # This threshold is based on observation only. There is no evidence about it. It can be changed if a better threshold is found
        truckFactor = []

        for name, ownDegree in ownership.items():
            if ownDegree >= truckFactorThreshold:
                truckFactor.append(name)

        print(f"Truck Factor: {truckFactor}, length: {len(truckFactor)}")
        entry                       = {}
        entry["repository_name"]    = repository_full_name
        entry["type"]               = "heuristic"
        entry["users"]              = truckFactor
        entry["truck_factor"]       = len(truckFactor)
        entry["date"]               = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        return entry

    def stack_based_truck_factor(self,repository_full_name):
        """
        Calculates the stack based truck factor for a given repository
        :param repository_full_name: The full name of the repository
        :return: array of users that build the truck factor
        """
        # those prints can stay here as they are not leaked to outside
        print(f"Calculating stack based truck factor for repository: {repository_full_name}")
        start_time = time.time()
        file_list = self.gaw.get_files(repository_full_name)
        end_time = time.time()
        print(f"Time taken to get file list: {end_time-start_time}")

        start_time = time.time()
        file_commits = self.gaw.get_file_commits(repository_full_name, file_list)
        end_time = time.time()
        print(f"Time taken to get file commits: {end_time-start_time}")

        file_commits = dict((k, v) for k, v in file_commits.items() if v) # We remove the empty arrays

        changeCount = {} # Number of commits of users
        fileCreator = {} # Creator of each file

        # k is the file name
        # v[i] is the each user that commited
        for k, v in file_commits.items():
            changeCount[k] = {}
            for i in range(0,len(v)):
                try:
                    changeCount[k][v[i]] += 1
                except:
                    changeCount[k][v[i]] = 1
                if i == (len(v) - 1): # Assumed first commited user is creator of file. Because of structure of json it is the last element
                    fileCreator[k] = v[i]

        changeCountExcept = {} # Number of commits except current user
        # k is the file name
        # key and a are the user names
        # b is the number of commits of user
        for k, v in changeCount.items():
            changeCountExcept[k] = {}
            for key in v.keys():
                changeCountExcept[k][key] = 0
                for a, b in v.items():
                    if a != key: # Because of we need other user's commit count. We don't include current user
                        changeCountExcept[k][key] += changeCount[k][a]

        doaValue = {} # Degree Of Author. Formula is from A_novel_approach_for_estimating_Truck_Factors.pdf
        totalDoa = {} # We need total doa of each file to normalize data
        totalFileCount = 0
        for k, v in changeCount.items():
            totalFileCount += 1
            doaValue[k] = {}
            for a, b in v.items():
                if a == fileCreator[k]:
                    fa = 1
                else:
                    fa = 0
                doaValue[k][a] = 3.293 + (1.098 * fa) + (0.164 * changeCount[k][a]) - (0.321 * math.log(1 + changeCountExcept[k][a]))
                # This formula is from pdf
                try:
                    totalDoa[k] = totalDoa[k] + doaValue[k][a]
                except:
                    totalDoa[k] = doaValue[k][a]

        authoredFiles = {}
        normalizeDoaTotal = {}
        for k, v in changeCount.items():
            for a, b in v.items():
                try:
                    normalizeDoaTotal[a] = normalizeDoaTotal[a] + (doaValue[k][a] / totalDoa[k])
                except:
                    normalizeDoaTotal[a] = doaValue[k][a] / totalDoa[k]


        sortedNormalizeDoa = {}
        for x in sorted(normalizeDoaTotal.items(), key=lambda a: a[1], reverse=True):
            sortedNormalizeDoa[x[0]] = normalizeDoaTotal[x[0]]

        truckFactor = []
        coverage = 0
        for k,v in sortedNormalizeDoa.items():
            truckFactor.append(k)
            coverage += v
            if coverage > (totalFileCount / 2): #If we looked half of the files than we break
                break

        print(f"Truck Factor: {truckFactor}, length: {len(truckFactor)}")
        entry                       = {}
        entry["repository_name"]    = repository_full_name
        entry["type"]               = "stack"
        entry["users"]              = truckFactor
        entry["truck_factor"]       = len(truckFactor)
        entry["date"]               = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        return entry

