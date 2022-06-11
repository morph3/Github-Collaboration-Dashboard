
from collections import Counter
import requests
import threading
import sys
import json

try:
    from src.Utils import *
except:
    from Utils import *

"""
Resources about Github REST API

https://docs.github.com/en/rest/overview/resources-in-the-rest-api#pagination

"""


class GithubAPIWrapper:
    """
    This is our own Github API Wrapper to make things easy
    """

    def __init__(self, token):
        self.token = token
        self.file_commits = {}

    def do_request(self, url):
        return requests.get(url, headers={'Authorization': f"token {self.token}"})

    def get_repository(self, repository_full_name):
        """
        Get information about the given repository
        """

        # Ex, https://api.github.com/repos/morph3/crawpy
        url = f"https://api.github.com/repos/{repository_full_name}"

        response = self.do_request(url)
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

    def get_commits(self, repository_full_name):
        """
        Get a list of commits for a given repository.

        https://docs.github.com/en/rest/overview/resources-in-the-rest-api#pagination
        https://blog.notfoss.com/posts/get-total-number-of-commits-for-a-repository-using-the-github-api/
        """
        # Ex,
        # https://api.github.com/repos/morph3/crawpy/commits
        url = f"https://api.github.com/repos/{repository_full_name}/commits"

        # this returns a list of json objects, each one represents a commit
        response = self.do_request(url)

        if response.status_code == 200:
            return response.json()
        else:
            return []

    def get_repositories(self, username):
        """
        Get a list of repositories for a given user.
        """
        url = f"https://api.github.com/users/{username}/repos"
        response = self.do_request(url)
        if response.status_code == 200:
            return response.json()
        else:
            return []

    def get_files(self, repository_full_name):
        """
        Get all the files in a given repository (full path) as a list

        An example of the return value is below,
        ['.gitignore', 'README.md', 'common.txt', 'crawpy.py', 'reports/template.html', 'requirements.txt', 'src/Banner.py', 'src/RequestEngine.py', 'src/__init__.py', 'src/config.py']
        """
        commits = self.get_commits(repository_full_name)
        # https://api.github.com/repos/morph3/crawpy/git/trees/f6bc50e364496e95422b9deb56a17d258c2b2d2c?recursive=1
        tree = commits[0]['commit']['tree']['url'] + "?recursive=1"

        response = self.do_request(tree)
        file_list = []
        if response.status_code == 200:
            # print(response.json())
            for file in response.json()["tree"]:
                if file["type"] == "blob":
                    file_list.append(file["path"])

            return file_list
        else:
            return []

    def get_file_commits(self, repository_full_name, file_list):
        """
        It looks like there is no other option than making those requests below so only performance gain we can get is making this function multi threaded.
        If we make this multithreaded we get blocked by github's rate limit so idk what to do.
        TODO:
            - Refactor this function, looks very ugly
        """

        """
        Get detailed commit information about the given file list and repository.

        It returns a dictionary like below,
            key: .gitignore, value: ['morph3']
            key: README.md, value: ['Melih Kaan Yıldız', 'morph3', 'morph3', 'morph3', 'morph3', 'morph3', 'morph3', 'morph3', 'morph3', 'morph3', 'morph3', 'morph3', 'morph3', 'morph3']
            key: common.txt, value: ['morph3', 'morph3']
            key: crawpy.py, value: ['morph3', 'morph3', 'morph3', 'morph3', 'morph3', 'morph3', 'morph3', 'morph3', 'morph3', 'morph3', 'morph3', 'morph3']
            key: reports/template.html, value: ['morph3', 'morph3', 'morph3']
            key: requirements.txt, value: ['morph3', 'morph3']
            key: src/Banner.py, value: ['morph3', 'morph3', 'morph3', 'morph3', 'morph3', 'morph3']
            key: src/RequestEngine.py, value: ['morph3', 'morph3', 'morph3', 'morph3', 'morph3', 'morph3', 'morph3', 'morph3', 'morph3', 'morph3', 'morph3', 'morph3', 'morph3', 'morph3', 'morph3', 'morph3', 'morph3', 'morph3', 'morph3']
            key: src/__init__.py, value: ['morph3']
            key: src/config.py, value: ['morph3', 'morph3', 'morph3', 'morph3', 'morph3', 'morph3', 'morph3', 'morph3', 'morph3']
        """

        #url_base = f"https://api.github.com/repos/{repository_full_name}/commits?path="

        self.file_commits = {}  # make sure its empty

        thread_list = []
        n_threads = 40
        for t in range(n_threads):
            t = threading.Thread(target=self.get_file_commits_helper, args=(
                repository_full_name, file_list,))
            thread_list.append(t)
            t.daemon = True
            t.start()

        for t in thread_list:
            try:
                t.join()
            except KeyboardInterrupt:
                print("[!] Keyboard interrupt recieved, exiting ...\n")
                sys.exit(1)
            except:
                pass
        return self.file_commits

    def get_file_commits_helper(self, repository_full_name, file_list):
        """
        Helper function for get_file_commits, it is called by get_file_commits to implement multi-threading.
        """
        url_base = f"https://api.github.com/repos/{repository_full_name}/commits?path="
        running = True
        while running:
            try:
                file = file_list.pop()
            except IndexError:
                running = False
                break

            url = url_base + file
            commits = self.do_request(url).json()
            try:
                self.file_commits[file] = []
                for commit in commits:
                    self.file_commits[file].append(
                        commit['commit']['author']['name'])
            except:
                pass

    def get_contributors(self, repository_full_name):

        page = 1
        contributors = []
        while True:
            url = f"https://api.github.com/repos/{repository_full_name}/contributors?per_page=1000&page={str(page)}"
            data = self.do_request(url).json()

            if len(data) == 0:
                break
            for element in data:
                if ("name" not in element):
                    if ("login" not in element):
                        break
                    else:
                        contributors.append(element["login"])
                else:
                    contributors.append(element["name"])

            page += 1

        return contributors

    def get_commit_count(self, repository_full_name, commit):
        """
        TODO: we might wanna add starting commit option as it only starts from the first commit

        Returns the commit count starting from the first commit to the given commit
        """
        fc = self.get_first_commit(repository_full_name)
        url = f"https://api.github.com/repos/{repository_full_name}/compare/{fc}...{commit}"
        commit_req = self.do_request(url)
        if commit_req.status_code == 200:
            commit_count = commit_req.json()['ahead_by'] + 1
            return commit_count
        else:
            return []

    def get_first_commit(self, repository_full_name):
        """
        Returns the hash of the first commit in the given repository.
        """

        url = f"https://api.github.com/repos/{repository_full_name}/commits"
        response = self.do_request(url)
        if response.status_code == 200:
            json_data = response.json()

            if response.headers.get('Link'):
                page_url = response.headers.get('Link').split(',')[1].split(';')[
                    0].split('<')[1].split('>')[0]
                commit_response = self.do_request(page_url)
                first_commit = commit_response.json()
                first_commit_hash = first_commit[-1]['sha']
                return first_commit_hash
            else:
                first_commit_hash = json_data[-1]['sha']
        else:
            return []

    def get_last_commit(self, repository_full_name):
        """
        Returns the hash of the last commit in the given repository.
        """
        url = f"https://api.github.com/repos/{repository_full_name}/git/refs/heads"
        response = self.do_request(url)
        if response.status_code == 200:
            foo = json.loads(response.text)
            for obj in foo:
                # yes main and master makes a huge difference right
                # you had to change the whole schema
                # such human rights, much justice, wow
                if ("refs/heads/master" in obj["ref"]) or ("refs/heads/main" in obj["ref"]):
                    last_commit_hash = obj['object']['sha']
                    return last_commit_hash
        else:
            return []

    def get_all_branch_names(self, repository_full_name):
        """Returns the branch list in the given repositories
        Args:
            repository_full_name (string): The repository links in format like "{username}/{repo}"

        Returns:
            branch_names : All branch names and informations about the branches in JSON format
        """

        url = f"https://api.github.com/repos/{repository_full_name}/branches"
        response = self.do_request(url)

        if response.status_code == 200:
            return response.json()
        else:
            return []

    def get_issues(self, repository_full_name):
        """Returns the issiues of a given repository name
        Args:
        r: Repo full name

        Returns:
        Issiues: JSON format of the issiues output of the GitHub API 
        """

        # we can get all the issues
        # so for example open issues ends in 3 pages,
        # https://api.github.com/repos/projectdiscovery/nuclei/issues?state=open&page=1
        # https://api.github.com/repos/projectdiscovery/nuclei/issues?state=open&page=2
        # https://api.github.com/repos/projectdiscovery/nuclei/issues?state=open&page=3

        # fetch closed issues like abowe as well.
        # After all the fetching is done, add all the issue objects together and return.

        # ooor
        # we can fetch closed and open issues like below,
        # https://api.github.com/search/issues?q=repo:projectdiscovery/nuclei+type:issue+state:open

        # open issues
        url = f"https://api.github.com/search/issues?q=repo:{repository_full_name}+type:issue+state:open"
        response = self.do_request(url)

        result = {}
        if response.status_code == 200:
            result["open_issues"] = response.json()["total_count"]
        else:
            return []

        # closed issues
        url = f"https://api.github.com/search/issues?q=repo:{repository_full_name}+type:issue+state:closed"
        response = self.do_request(url)

        if response.status_code == 200:
            result["closed_issues"] = response.json()["total_count"]
        else:
            return []

        return result

    def get_contributions(self, repository_full_name):
        """
        Returns the contributions of a given repository name
        Args:
        repository_full_name: Repo full name

        Returns:
        Contributions: JSON format of the contributions output of the GitHub API 

        """

        # https://api.github.com/repos/projectdiscovery/nuclei/contributors

        # this per_page is a temporary fix, it might get f'd up with repositories that have huge number of contributors
        url = f"https://api.github.com/repos/{repository_full_name}/contributors?per_page=1000"
        response = self.do_request(url)

        """
        response["login"] is the username
        response["contributions"] is the number of contributions
        """

        if response.status_code == 200:
            return response.json()
        else:
            return []

    def commit_based_gini_index(self, repository_full_name):

        commit_numbers = []
        contributions = self.get_contributions(repository_full_name)

        for i in contributions:

            commit_numbers.append(i["contributions"])
            # print(i["contributions"])

        return calculate_gini_index(commit_numbers)

    # functions that takes the repsitory name and returns the distribution of issues

    def issue_based_gini_index(self, repository_full_name):

        # Take the open issues
        url = f"https://api.github.com/search/issues?q=repo:{repository_full_name}+type:issue+state:open"
        response = self.do_request(url)

        result = []
        for i in response.json()["items"]:
            result.append(i["user"]["login"])

        # Same thing for closed issues
        url = f"https://api.github.com/search/issues?q=repo:{repository_full_name}+type:issue+state:closed"
        response = self.do_request(url)

        for i in response.json()["items"]:
            result.append(i["user"]["login"])

        # Result array is now filled with all the usernames, now we need to count the number of times each username appears
        result = list(Counter(result).values())

        return calculate_gini_index(result)
