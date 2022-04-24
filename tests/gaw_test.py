import unittest
import sys
import os
sys.path.append(os.getcwd() + '/../src/')

from GithubAPIWrapper import *


class TestGithubAPIWrapper(unittest.TestCase):
    def test_get_repository_info(self):
        with open("../.env", "r") as f:
            token = f.read().split("=")[1].strip()
        gaw = GithubAPIWrapper(token)
        
        repo_full_name = "projectdiscovery/httpx"
        repo = gaw.get_repository(repository_full_name=repo_full_name)
        self.assertEqual(repo["html_url"], "https://github.com/projectdiscovery/httpx")

    def test_another(self):
        pass


if __name__ == "__main__":

    unittest.main()
    
    """
    TODO: convert below to unit tests
    
    For testing purposes
    token = open("../.env", "r").read().split("=")[1].strip()
    gaw = GithubAPIWrapper(token)

    rn = "xct/ropstar"
    rn = "apexcharts/apexcharts.js"
    rn = "SerenityOS/serenity"
    rn = "morph3/crawpy"

    fc = gaw.get_first_commit(rn)
    print(f"First commit: {fc}")
    lc = gaw.get_last_commit(rn)
    print(f"Last commit: {lc}")
    count = gaw.get_commit_count(rn, lc)
    print(f"Commit count for {rn}: {count}")

    bn = gaw.print_branch_list(rn)
    print(f"Branch list for {rn}: {bn}")

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
    """
