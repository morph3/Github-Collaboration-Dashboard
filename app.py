import flask
import requests
import sys
import os
import json

from collections import Counter

from src.TruckFactor import TruckFactorCalculator
from src.GithubAPIWrapper import GithubAPIWrapper


# global variables for the app
ENV = {}
TRUCK_FACTOR_CACHE = ""
CACHE_FILE = None
CACHE_NAME = "cache.json"


def dot_env_parser():
    """ Function to parse the .env file and store the values in a dictionary.

    Args:
        None

    Returns:
        None
    """
    f = open(".env", "r").read()
    for line in f.splitlines():
        k, v = line.split("=")
        ENV[k] = v


def check_cache(repo_name, type):
    """ Function to check if the cache is empty or not.

    Args:
        repo_name (string): The name of the repository.
        type (string): The type of the repository.

    Returns:
        bool: True if the cache is empty, False otherwise.
    """
    # if the cache is empty return None
    if TRUCK_FACTOR_CACHE == "":
        return None

    # check if the entry is in the cache
    for item in TRUCK_FACTOR_CACHE:
        try:
            if (item["repository_name"] == repo_name) and (item["type"] == type):
                print(
                    f"We found a match in the cache for {repo_name} with type {type}")
                print(item)
                return item
        except:
            continue
    return None


def update_cache(entry):
    """ Function to update the cache.

    Args:
        entry (dict): The entry to be added to the cache.

    Returns:
        None
    """

    # if the cache is empty
    if TRUCK_FACTOR_CACHE == "":
        CACHE_FILE = open(CACHE_NAME, "w")
        CACHE_FILE.write(entry)
        CACHE_FILE.close()

    # append the given entry(dict)
    TRUCK_FACTOR_CACHE.append(entry)
    CACHE_FILE = open(CACHE_NAME, "w")
    CACHE_FILE.write(json.dumps(TRUCK_FACTOR_CACHE))

    # remove the oldest entry
    # TODO: remove the oldest entry in the cache
    return


# create the flask app, and set the port (default port is 5000)
app = flask.Flask(__name__)


# index route, which will be called when the user goes to the root of the website
@app.route('/')
def index():
    # return the index.html file, which is the main page of the website
    return flask.render_template('index.html')


# route to get the truck factor for a given repository
@app.route('/repository')
def repository_search():

    repository_full_name = flask.request.args.get('r')
    repository_info = gaw.get_repository(repository_full_name)
    #TruckFactor.get_repository(repository_info, ENV['GITHUB_TOKEN'])
    commits = gaw.get_commits(repository_full_name)
    lc = gaw.get_last_commit(repository_full_name)
    number_of_commits = gaw.get_commit_count(repository_full_name, lc)

    issue_info = gaw.get_issues(repository_full_name)

    # not a good solution but, let's just append it for now
    repository_info["number_of_commits"] = number_of_commits
    # not a good solution but, let's just append it for now
    repository_info["open_issues"] = issue_info["open_issues"]
    # not a good solution but, let's just append it for now
    repository_info["closed_issues"] = issue_info["closed_issues"]

    # render the repository.html file, which will display the repository information
    return flask.render_template('repo-based.html', repository_info=repository_info)

# route to get the truck factor for a given user and repository


@app.route('/user')
def user_search():
    username = flask.request.args.get('u')
    repos = gaw.get_repositories(username)
    return flask.render_template('user-based.html', username=username, repositories=repos)


@app.route('/api/get_repository_info')
def get_repository_info():
    """
    This should take GET parameters r, and return repository information in json format

    """
    l = {}

    repo_full_name = flask.request.args.get('r')
    l["Information"] = gaw.get_repository(repository_full_name=repo_full_name)

    return json.dumps(l, indent=4)

# Endpoint to get the repository commits for a given repository


@app.route('/api/get_repository_commits')
def get_repository_commits():
    """
    This should take GET parameter r and return commits of a repository in json format
    """
    l = []

    repo_full_name = flask.request.args.get('r')

    commits = gaw.get_commits(repository_full_name=repo_full_name)

    # For each commit, get the commit information
    for i in commits:
        # Each line, Takes commiters' infos and commmit messages
        l.append({"commiter": i["commit"]["committer"],
                  "commit": i["commit"]["message"]})

    return json.dumps(l, indent=4)

# Endpoint to get the user repositories for a given user


@app.route('/api/get_user_repositories')
def get_user_repositories():
    """
    This should take GET parameter u and return repositories in json format
    """
    l = {}

    username = flask.request.args.get('u')
    repos = gaw.get_repositories(username)

    l['username'] = username
    l['Repositories'] = [i['name'] for i in repos]

    return json.dumps(l, indent=4)

# Endpoint to calculate the truck factor for a given repository with the given username


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
    cached_entry = check_cache(repository_full_name, type)

    tfc = TruckFactorCalculator(gaw)

    if type == "commit":

        # if is_force is set to true, calculate the tf and cache it
        if (is_force == "true"):
            result = tfc.commit_based_truck_factor(repository_full_name)
            update_cache(result)
            # do the caching
        else:
            # if the is force is not set,
            #
            # check if the tf is in the cache
            if(cached_entry):
                print(f"We hit the cache with: {cached_entry}")
                result = cached_entry
            # if it's not in the cache, calculate it and cache it
            else:
                result = tfc.commit_based_truck_factor(repository_full_name)
                update_cache(result)

        print(f"Returning {json.dumps(result)}")
        # result should already be in the format of json
        return json.dumps(result), {"Content-Type": "application/json"}

<<<<<<< Updated upstream
    elif type == "blame":
        return "{\"error\": \"blame not implemented yet\"}"

=======
>>>>>>> Stashed changes
    elif type == "heuristic":

        # if is_force is set to true, calculate the tf and cache it
        if (is_force == "true"):
            result = tfc.heuristic_based_truck_factor(repository_full_name)
            update_cache(result)
            # do the caching
        else:
            # if the is force is not set,
            #
            # check if the tf is in the cache
            if(cached_entry):
                result = cached_entry
            # if it's not in the cache, calculate it and cache it
            else:
                result = tfc.heuristic_based_truck_factor(repository_full_name)
                update_cache(result)
<<<<<<< Updated upstream
        # result should already be in the format of json
        return json.dumps(result), {"Content-Type": "application/json"}
=======
        return json.dumps(result) , {"Content-Type":"application/json"} # result should already be in the format of json

    elif type == "stack":

        # if is_force is set to true, calculate the tf and cache it
        if (is_force == "true"):
            result = tfc.stack_based_truck_factor(repository_full_name)
            update_cache(result)
            # do the caching
        else:
            # if the is force is not set,
            #
            #check if the tf is in the cache
            if(cached_entry):
                result = cached_entry
            # if it's not in the cache, calculate it and cache it
            else:
                result = tfc.stack_based_truck_factor(repository_full_name)
                update_cache(result)
        return json.dumps(result) , {"Content-Type":"application/json"} # result should already be in the format of json

>>>>>>> Stashed changes
    return "{\"error\": \"Given truck factor is not found\"}"

# Endpoint to get issues for a given repository


@app.route('/api/get_issues')
def get_issues():
    """
    Args:
    r: Repo full name

    Return: 
    issues: a list of issues in json format, it should include an entry for each issue whether it is closed or not
    it can have more additional entries as well
    """
    repo_full_name = flask.request.args.get('r')

    issues = gaw.get_issues(repo_full_name)

    return json.dumps(issues), {"Content-Type": "application/json"}

# Endpoint to get the number of branches for a given repository with commits


@app.route('/api/get_branches')
def get_branches():
    """
    Args:
    r: repository full name

    Return:
    branch_names : a list of json objects where each object contains the name of the branch, commit and protected field
    """
    l = {}

    repo_full_name = flask.request.args.get('r')

    branch_names = gaw.get_all_branch_names(repo_full_name)

    return json.dumps(branch_names), {"Content-Type": "application/json"}

# Endpoint to get the commit distribution for a given repository


@app.route('/api/get_commit_distribution')
def get_commit_distribution():
    # https://api.github.com/repos/projectdiscovery/nuclei/contributors
    """
    Args: 
    r: Repo full name

    :Return 
    commit_distribution: a json object, it should contain a list users and their commit count
    """

    repo_full_name = flask.request.args.get('r')

    contributions = gaw.get_contributions(repo_full_name)

    return json.dumps(contributions), {"Content-Type": "application/json"}


"""
TODO: write needed api routes following the pattern above
"""

# Endpoint to test new features in the app


@app.route('/test')
def test():
    return flask.render_template('test.html')


# Endpoint to get number of contributors for a given repository
@app.route('/api/get_number_of_contributors')
def get_number_of_contributors():
    """
    Args:
    r: Repo full name

    :Return
    number of contributers: a json object that contains count of total number of contributers, ex: {"number_of_contributers":2}
    """
    repo_full_name = flask.request.args.get('r')
    result = gaw.get_contributors(repo_full_name)

    return json.dumps({"number_of_contributers": len(result)})


# if the file is run directly, run the app
if __name__ == '__main__':
    dot_env_parser()

    # if the cache.json file exists, load it
    if os.path.exists(CACHE_NAME):
        CACHE_FILE = open(CACHE_NAME, "r")  # array of json objects
        TRUCK_FACTOR_CACHE = json.loads(CACHE_FILE.read())

    gaw = GithubAPIWrapper(ENV["GITHUB_TOKEN"])

    app.run(debug=True, port=5000, threaded=True)
