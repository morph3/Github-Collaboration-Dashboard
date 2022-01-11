import requests
import threading
import sys

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

        url = f"https://api.github.com/repos/{repository_full_name}" # Ex, https://api.github.com/repos/morph3/crawpy

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
        tree = commits[0]['commit']['tree']['url'] + "?recursive=1" # https://api.github.com/repos/morph3/crawpy/git/trees/f6bc50e364496e95422b9deb56a17d258c2b2d2c?recursive=1

        response = self.do_request(tree)
        file_list = []
        if response.status_code == 200:
            #print(response.json())
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

        #file_commits = {}

        thread_list = []
        n_threads = 50
        for t in range(n_threads):
            t = threading.Thread(target=self.get_file_commits_helper, args=(repository_full_name,file_list,))
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

    def get_file_commits_helper(self,repository_full_name,file_list):
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
                    self.file_commits[file].append(commit['commit']['author']['name'])
            except:
                pass

    def get_contributors(self,repository_full_name):

        page = 1
        contributors = []
        while True:
            url = f"https://api.github.com/repos/{repository_full_name}/contributors?per_page=1000&page="+str(page)+"&anon=1"
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

            page+=1

        return contributors


if __name__ == "__main__":
    """
    For testing purposes
    """
    gaw = GithubAPIWrapper("")
    repository_info = gaw.get_repository("morph3/crawpy")
    #commits = gaw.get_commits("morph3/crawpy")
    files = gaw.get_files("morph3/crawpy")
    #files = ['.gitignore', 'README.md', 'common.txt', 'crawpy.py', 'template.html', 'requirements.txt', 'Banner.py', 'RequestEngine.py', '__init__.py', 'config.py']
    print(files)
    file_commits = gaw.get_file_commits("morph3/crawpy", files)
    print(file_commits)

    file_commits = dict((k, v) for k, v in file_commits.items() if v) # We remove the empty arrays
    print(file_commits)
    for k,v in file_commits.items():
        print(f"key: {k}, value: {v}")
