import flask
import requests
import sys
from src.TruckFactor import TruckFactorCalculator
from src.GithubAPIWrapper import GithubAPIWrapper

ENV = {}
def dot_env_parser():
    f = open(".env","r").read()
    for line in f.splitlines():
        k, v = line.split("=")
        ENV[k] = v

app = flask.Flask(__name__)

# index route
@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/repository')
def repository_search():
    
    repository_full_name = flask.request.args.get('r')
    repository_info = gaw.get_repository(repository_full_name)
    #TruckFactor.get_repository(repository_info, ENV['GITHUB_TOKEN'])
    commits = gaw.get_commits(repository_full_name)
    number_of_commits = len(commits)
    repository_info["number_of_commits"] = number_of_commits # not a good solution but, let's just append it for now
    return flask.render_template('repo-based.html', repository_info=repository_info )


@app.route('/user')
def user_search():
    username = flask.request.args.get('u')
    repos = gaw.get_repositories(username)
    return flask.render_template('user-based.html', username=username, repositories=repos)


@app.route('/api/get_repository_info')
def get_repository_info():
    """
    This should take GET parameter r and return repository information in json format
    """
    pass


@app.route('/api/get_repository_commits')
def get_repository_commits():
    """
    This should take GET parameter r and return commits of a repository in json format
    """
    pass


@app.route('/api/get_user_repositories')
def get_user_repositories():
    """
    This should take GET parameter u and return repositories in json format
    """
    pass


@app.route('/api/calculate_truck_factor')
def calculate_truck_factor():
    """
    This should take GET parameter r and t and return truck factor result of type t in json format including who forms the truck factor 
    """
    pass


"""
TODO: write needed api routes following the pattern above 
"""





if __name__ == '__main__':
    dot_env_parser()
    gaw = GithubAPIWrapper(ENV["GITHUB_TOKEN"])

    app.run(debug=True, port=5000, threaded=True)
