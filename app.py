import flask
import requests
import sys
import os
import json

from collections import Counter
from src.TruckFactor import TruckFactorCalculator
from src.GithubAPIWrapper import GithubAPIWrapper
from src.Utils import *
from src.DataStorage import SimpleStorage

# global variables
ENV                 = {}
storage             = None
storage_filename    = "storage.json"
app                 = flask.Flask(__name__)

# index route
@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/repository')
def repository_search():

    repository_full_name                    = flask.request.args.get('r')
    repository_info                         = gaw.get_repository(repository_full_name)
    #TruckFactor.get_repository(repository_info, ENV['GITHUB_TOKEN'])
    commits                                 = gaw.get_commits(repository_full_name)
    lc                                      = gaw.get_last_commit(repository_full_name)
    number_of_commits                       = gaw.get_commit_count(repository_full_name, lc)
    issue_info                              = gaw.get_issues(repository_full_name)
    repository_info["number_of_commits"]    = number_of_commits # not a good solution but, let's just append it for now
    repository_info["open_issues"]          = issue_info["open_issues"]
    repository_info["closed_issues"]        = issue_info["closed_issues"]
    return flask.render_template('repo-based.html', repository_info=repository_info)


@app.route('/user')
def user_search():
    username    = flask.request.args.get('u')
    repos       = gaw.get_repositories(username)
    return flask.render_template('user-based.html', username=username, repositories=repos)


@app.route('/api/get_repository_info')
def get_repository_info():
    """
    This should take GET parameters r, and return repository information in json format

    """
    l                = {}
    repo_full_name   = flask.request.args.get('r')
    l["Information"] = gaw.get_repository(repository_full_name= repo_full_name)
    return json.dumps(l,indent=4)


@app.route('/api/get_repository_commits')
def get_repository_commits():
    """
    This should take GET parameter r and return commits of a repository in json format
    """
    l               = []
    repo_full_name  = flask.request.args.get('r')
    commits         = gaw.get_commits(repository_full_name= repo_full_name)

    for i in commits:
        #Each line, Takes commiters' infos and commmit messages
        l.append( {"commiter":i["commit"]["committer"], "commit": i["commit"]["message"] } )

    return json.dumps(l, indent=4)


@app.route('/api/get_user_repositories')
def get_user_repositories():
    """
    This should take GET parameter u and return repositories in json format
    """
    l           = {}
    username    = flask.request.args.get('u')
    repos       = gaw.get_repositories(username)


    l['username']       = username
    l['Repositories']   = [i['name'] for i in repos]

    return json.dumps(l, indent=4)


@app.route('/api/calculate_truck_factor')
def calculate_truck_factor():
    """
    :args r: repository full name
    :args t: type of the repository
    :returns: a json object of calculated truck factor, including repository name, tf, users and type
    """

    type = flask.request.args.get('t')
    repository_full_name = flask.request.args.get('r')
    is_force = flask.request.args.get('force')
    print(f"Is force: {is_force}")
    
    storage_entry = storage.get_last(repository_full_name, type) 


    tfc = TruckFactorCalculator(gaw)

    if type == "commit":
        
        # if the is_force is true, recalcualate the truck factor and add it to storage no matter what
        if (is_force == "true"):
            result = tfc.commit_based_truck_factor(repository_full_name)
            storage.add(result)

        else:
            # if is_force is false but there is an entry in the storage, return that entry
            if(storage_entry):
                print(f"We hit the cache with: {storage_entry}")
                result = storage_entry

            else:
                # if there is no entry in the storage, calculate the truck factor and add it to the storage
                result = tfc.commit_based_truck_factor(repository_full_name)
                storage.add(result)

        print(f"Returning {json.dumps(result)}")
        return json.dumps(result), {"Content-Type":"application/json"} # result should already be in the format of json

    elif type == "stack":

        if (is_force == "true"):
            result = tfc.stack_based_truck_factor(repository_full_name)
            storage.add(result)

        else:
            if(storage_entry):
                result = storage_entry

            else:
                result = tfc.stack_based_truck_factor(repository_full_name)
                storage.add(result)
        return json.dumps(result) , {"Content-Type":"application/json"} # result should already be in the format of json



    elif type == "heuristic":

        if (is_force == "true"):
            result = tfc.heuristic_based_truck_factor(repository_full_name)
            storage.add(result)

        else:
            if(storage_entry):
                result = storage_entry
            else:
                result = tfc.heuristic_based_truck_factor(repository_full_name)
                storage.add(result)
        return json.dumps(result) , {"Content-Type":"application/json"} # result should already be in the format of json
    
    return "{\"error\": \"Given truck factor is not implemented yet\"}"


@app.route('/api/get_issues')
def get_issues():
    """
    Args:
    r: Repo full name

    Return:
    issues: a list of issues in json format, it should include an entry for each issue whether it is closed or not
    it can have more additional entries as well
    """

    repo_full_name  = flask.request.args.get('r')
    issues          = gaw.get_issues(repo_full_name)

    return json.dumps(issues), {"Content-Type":"application/json"}

@app.route('/api/get_branches')
def get_branches():
    """
    Args:
    r: repository full name

    Return:
    branch_names : a list of json objects where each object contains the name of the branch, commit and protected field
    """
    repo_full_name  = flask.request.args.get('r')
    branch_names    = gaw.get_all_branch_names(repo_full_name)

    return json.dumps(branch_names), {"Content-Type":"application/json"}


@app.route('/api/get_commit_distribution')
def get_commit_distribution():
    # https://api.github.com/repos/projectdiscovery/nuclei/contributors

    """
    Args:
    r: Repo full name

    :Return
    commit_distribution: a json object, it should contain a list users and their commit count
    """

    repo_full_name  = flask.request.args.get('r')
    contributions   = gaw.get_contributions(repo_full_name)

    return json.dumps(contributions), {"Content-Type":"application/json"}



@app.route('/api/get_number_of_contributors')
def get_number_of_contributors():
    """
    Args:
    r: Repo full name

    :Return
    number of contributers: a json object that contains count of total number of contributers, ex: {"number_of_contributers":2}
    """
    repo_full_name  = flask.request.args.get('r')
    result          = gaw.get_contributors(repo_full_name)

    return json.dumps({"number_of_contributers":len(result)})

@app.route('/api/get_gini_index')
def get_gini_index():
    """
    Args:
    r: Repo full name

    :Return
    gini_index: a json object that contains gini index of the repository
    """
    repo_full_name  = flask.request.args.get('r')
    result          = gaw.get_gini_index(repo_full_name)

    return json.dumps({"gini_index":result})


@app.route('/api/get_issue_distribution')
def get_issue_dist():
    
    repo_full_name  = flask.request.args.get('r')
    result          = gaw.get_issue_distribution(repo_full_name)
    
    
    return json.dumps({'issue_dist':result})


@app.route('/api/get_issue_gini_index')
def get_issue_gini_index():
    repo_full_name  = flask.request.args.get('r')
    result          = gaw.get_issue_gini_index(repo_full_name)

    return json.dumps({'issue_gini_index':result})



@app.route('/api/get_truck_factor_history')
def get_truck_factor_history():
    """
    :args r: repository full name
    :args t: type of the repository
    :returns: a json object of calculated truck factor, including repository name, tf, users and type
    """
    
    type                    = flask.request.args.get('t')
    repository_full_name    = flask.request.args.get('r')
    storage_entry           = storage.get_all(repository_full_name, type) 

    return json.dumps(storage_entry), {"Content-Type":"application/json"}



@app.route('/test')
def test():
    return flask.render_template('test.html')



if __name__ == '__main__':
    
    ENV = dot_env_parser()

    # if the storage.json file exists, load it 
    if os.path.exists(storage_filename):
        storage = SimpleStorage()
        storage.load_file(storage_filename)

    gaw = GithubAPIWrapper(ENV["GITHUB_TOKEN"])
    app.run(debug=True, port=5000, threaded=True)
