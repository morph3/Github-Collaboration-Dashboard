import requests
import operator
import math

def get_repository(repository_info, token):
    url = repository_info['commits_url']
    url = url[:-6]
    commits = (requests.get(url, headers={'Authorization': 'token {}'.format(token)})).json()
    files_url = commits[0]['commit']['tree']['url']

    fileList = []
    get_files(files_url, token, fileList)

    calculateAvlTF(repository_info['full_name'], token, fileList)

def get_files(url, token, fileList):
    files = (requests.get(url, headers={'Authorization': 'token {}'.format(token)})).json()
    for file in files['tree']:
        if file['type'] == 'blob':
            fileList.append(file['path'])
        elif file['type'] == 'tree': # If it contains any folder
            get_files(file['url'], token, fileList)

def calculateAvlTF(full_name, token, fileList):

    url_base = "https://api.github.com/repos/"+full_name+"/commits?path="

    file_commits = {}
    for file in fileList:
        url = url_base + file
        commits = (requests.get(url, headers={'Authorization': 'token {}'.format(token)})).json()
        try:
            file_commits[file] = []
            for commit in commits:
                file_commits[file].append(commit['commit']['author']['name'])
        except:
            pass

    file_commits = dict((k, v) for k, v in file_commits.items() if v) # We remove the empty arrays

    changeCount = {} #Number of commits of users
    fileCreator = {} #Creator of each file

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
    for x in sorted(authoredFiles, key=operator.itemgetter(0)):
        sortedAuthoredFiles[x] = authoredFiles[x]

    truckFactor = []
    coverage = 0
    for k,v in sortedAuthoredFiles.items():
        truckFactor.append(k)
        coverage -= v
        if coverage < (totalFileCount / 2): #If we looked half of the files than we break
            break

    print("Truck Factor: " + str(len(truckFactor)))
    print(truckFactor)