import flask
import requests
import sys

ENV = {}
def dot_env_parser():
    f = open(".env","r").read()
    for line in f.splitlines():
        k, v = line.split("=")
        ENV[k] = v

app = flask.Flask(__name__)


def get_repository(repository_full_name):
    """
    Get information about the given repository
    """

    url = 'https://api.github.com/repos/{}'.format(repository_full_name) # Ex, https://api.github.com/repos/morph3/crawpy
    
    response = requests.get(url, headers={'Authorization': 'token {}'.format(ENV['GITHUB_TOKEN'])})
    """
    stargazers_count -> number of stars
    watchers_count -> number of watchers
    forks_count -> number of forks
    open_issues_count -> number of open issues
    owner.avatar_url -> url to the avatar image > we can use this to get the image for a better display
    """
    if response.status_code == 200:
        return response.json()
    else:
        return []

def get_commits(username, repository_name):
    """
    Get a list of commits for a given repository.
    """
    # Ex,
    # https://api.github.com/repos/morph3/crawpy/commits
    url = 'https://api.github.com/repos/{}/{}/commits'.format(username, repository_name) 
    
    # this returns a list of json objects, each one represents a commit
    response = requests.get(url, headers={'Authorization': 'token {}'.format(ENV['GITHUB_TOKEN'])})
    
    if response.status_code == 200:
        return response.json()
    else:
        return []

def get_repositories(username):
    """
    Get a list of repositories for a given user.
    """
    url = 'https://api.github.com/users/{}/repos'.format(username)
    response = requests.get(url, headers={'Authorization': 'token {}'.format(ENV['GITHUB_TOKEN'])})
    if response.status_code == 200:
        return response.json()
    else:
        return []




# index route
@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/repository')
def repository_search():
    
    repository_full_name = flask.request.args.get('r')
    username = repository_full_name.split('/')[0]
    repository_name = repository_full_name.split('/')[1]
    
    repository_info = get_repository(repository_full_name)
    
    commits = get_commits(username, repository_name)
    number_of_commits = len(commits)
    repository_info["number_of_commits"] = number_of_commits # not a good solution but, let's just append it for now
    return flask.render_template('repo-based.html', repository_info=repository_info )


@app.route('/user')
def user_search():
    username = flask.request.args.get('u')
    repos = get_repositories(username)
    return flask.render_template('user-based.html', username=username, repositories=repos)


if __name__ == '__main__':
    dot_env_parser()
    app.run(debug=True, port=5000, threaded=True)
