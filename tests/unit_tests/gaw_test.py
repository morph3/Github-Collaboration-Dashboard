import unittest
import sys
import os
sys.path.append(os.getcwd() + '/src/')

from GithubAPIWrapper import *


class TestGithubAPIWrapper(unittest.TestCase):
    
# test case for check the method can get the repository information
    def test_get_repository_info(self):
        with open(os.getcwd() + "/.env", "r") as f:
            token = f.read().split("=")[1].strip()
        gaw = GithubAPIWrapper(token)
        
        # you can change the repository name here
        repo_full_name = "projectdiscovery/httpx"
        
        # run the method
        repo = gaw.get_repository(repository_full_name=repo_full_name)
        
        # test case is true when repository URL is same as the one in the result of the method 
        self.assertEqual(repo["html_url"], "https://github.com/projectdiscovery/httpx")

# test case for check the method can get the user information
    def test_get_user_info(self):
        with open(os.getcwd() + "/.env", "r") as f:
            token = f.read().split("=")[1].strip()
        gaw = GithubAPIWrapper(token)
        
        # you can change the user name here
        username = "Seqat"
        
        # run the method
        user = gaw.get_user(username=username)
        
        # test case is true when username is same as the one in the result of the method 
        self.assertEqual(username, user["login"])

# test case to check the method can get the repository list of a selected user (only public repositories)
    def test_get_repositories(self):
        with open(os.getcwd() + "/.env", "r") as f:
            token = f.read().split("=")[1].strip()
        gaw = GithubAPIWrapper(token)
        
        # you can change the user name and repositories here
        username = "Seqat"
        
        result_repos= ["codespace_test","HackerRankSolution"]
        
        # run the method
        repos = gaw.get_repositories(username=username)
        
        #take only the name of the repositories (trim the response)
        repos = [x["name"] for x in repos]
        
        
        #the test case is true when the result of the method is same as the result_repos
        self.assertTrue(result_repos[i]==repos[i] for i in range(len(result_repos)))

# test case to check contributos of a selected repository
    def test_get_contributors(self):
        with open(os.getcwd() + "/.env", "r") as f:
            token = f.read().split("=")[1].strip()
        gaw = GithubAPIWrapper(token)
        
        # you can change the full repository name and the contributor list here
        repo_full_name = "apexcharts/apexcharts.js"
        
        
        contributor_list = [   'junedchhipa', 'tianxie1995', 'sergkop', 'dependabot[bot]', 'DavidMarquezF', 'ordago', 'fracz', 'github-rj', 'brianlagunas', 'kdinev', 'AurelReb', 'innocenzi', 'spotman', 'etresoft', 'shiroemons', 'styd', 'gsisso', 'jessecrossley', 'LeaVerou', 'mikaelkaron', 'thijscrombeen', 'karna48', 'jzonta', 'MartinKravec', 'rubenstolk', 'SielloRiatto', 'cola119', 'JCQuintas', 'onmotion', 'AlfieJ', 'jimfilippou', 'madza91',
                        'nekitk', 'Radix1', 'rantecki', 'strixy', 'TheDoctor0', 'tomohirohiratsuka', 'zur4ik', 'grinat', 'schottey', 'evjenio', 'Alex-Sokolov', 'ahocevar3tav', 'andresmrm', 'cailloumajor', 'bnymncoskuner', 'cstlaurent', 'clauso', 'Clint-Chester', 'sourcecodeit', 'doronguttman', 'Jinksi', 'f0rb1d', 'FunkiR', 'isy', 'jchamb', 'jaksim', 'JamieSlome', 'johndab', 'jnncks', 'joadan', 'illandril', 'jliit', 'Junich10', 'KYDronePilot', 'kevinehosford', 'KylePinkerton', 'lucalves', 'MarieR12', 'marilii-saar', 'mark-langer', 'mattkhaw', 'MaxLeiter', 'oguzhaninan', 'OriginalEXE', 'pnorbi-bp-grape', 'philfontaine', 'pierre-alain-b', 'praneetloke', 'kgram007', 'rndmerle', 'koljada', 'romanetsdev', 'saharak-manoo', 'sakshampuri', 'cubemastercodes', 'snemvalts', 'sebastianbassen', 'sbke-mms', 'slara', 'simonepri', 'rummanhasnayeen', 'tjveldhuizen', 'tkieft', 'tgpoint', 'nadvornik', 'razorness', 'Warix3', 'YogliB', 'actus-wirtenberger', 'zieu', 'arjunshibu', 'cemujax', 'franklx', 'garyptse', 'gdenhez42', 'gkristin', 'heartbeatLV', 'HesamZamanpour',
                        'jchang19', 'jmformenti-aia', 'lf94', 'solufa', 'marvin-j97', 'mestaritonttu', 'pablopsp', 'ralmeida-espatial', 'llmora', 'venarius', 'yangkun', 'yrajabi', 'joe94113']
        
        
        # run the method
        contributors = gaw.get_contributors(repository_full_name=repo_full_name)
        
        # the test is true when the result of the method is same as the cont_list
        self.assertTrue(contributor_list[i]==contributors[i] for i in range(len(contributor_list)))


# test case to cjheck the method can get the first commit hash of a selected repository
    def test_get_first_commit(self):
        with open(os.getcwd() + "/.env", "r") as f:
            token = f.read().split("=")[1].strip()
        gaw = GithubAPIWrapper(token)
        
        # you can change the full repository name and the first commit hash here
        repo_full_name  = "Seqat/HackerRankExercises"
        
        test_hash = "b07601f15fc9fcb09e9dc7d778e47de5203c3782"
        
        # take the first commit of the repository
        first_commit    = gaw.get_first_commit(repository_full_name=repo_full_name)
        
        # the test is true when the result of the method is same as the test_hash
        self.assertEqual(test_hash, first_commit)

# test case to check the method can get the last commit hash of a selected repository
    def test_get_last_commit(self):
        with open(os.getcwd() + "/.env", "r") as f:
            token = f.read().split("=")[1].strip()
        gaw = GithubAPIWrapper(token)
        
        # you can change the full repository name and the last commit hash here
        repo_full_name  = "Seqat/HackerRankExercises"
        
        test_hash = "8ea2a7818d65b30bc2de220d251e01f18bc4de5a"
        
        # take the last commit of the repository
        last_commit    = gaw.get_last_commit(repository_full_name=repo_full_name)

        # the test is true when the result of the method is same as the test_hash
        self.assertEqual(test_hash, last_commit)

# test case to check the method can get the commit count of a selected repository
    def test_get_commit_count(self):
        with open(os.getcwd() + "/.env", "r") as f:
            token = f.read().split("=")[1].strip()
        gaw = GithubAPIWrapper(token)
        
        # you can change the full repository name and the commit count here
        repo_full_name = "Seqat/HackerRankExercises"
        count=46
        
        # get the last commit of the repository to run the method properly
        last_commit= gaw.get_last_commit(repository_full_name=repo_full_name)
        
        # run the method
        commit_count = gaw.get_commit_count( repository_full_name=repo_full_name, commit=last_commit)
        
        # the test is true when the result of the method is same as the cont_list
        self.assertEqual(commit_count,count)


# test case to check the method can get all the branches of a selected repository
    def test_get_branches(self):
        with open(os.getcwd() + "/.env", "r") as f:
            token = f.read().split("=")[1].strip()
        gaw = GithubAPIWrapper(token)
        
        # you can change the full repository name and the branch list here
        repo_full_name = "xct/go-sqlite3"
        
        test_branches = [   'csv', 'feature-pointer-callback', 'fix-635', 'fix-688', 'fix-build2', 'fix-variadic', 'fix-vet', 'gh-pages',
                            'master', 'noncgo', 'notify', 'see', 'sqlite-amalgamation-3280000', 'sqlite-amalgamation-3290000', 'systemlib', 'type']
        
        # run the method and trims the branch names
        branches= gaw.get_all_branch_names(repository_full_name=repo_full_name)
        branches= [x['name'] for x in branches]
        
        # test is true when the result of the method is same as the test_branches
        self.assertTrue(branches[i]==test_branches[i] for i in range(len(test_branches)))


# test case to check the method can give the number of issues of a selected repository
    def test_get_issues_count(self):
        with open(os.getcwd() + "/.env", "r") as f:
            token = f.read().split("=")[1].strip()
        gaw = GithubAPIWrapper(token)

        # you can change the full repository name and the issue counts here
        repo_full_name = "SerenityOS/serenity"
        
        test_issues = {"open_issues": 506, "closed_issues": 2495}
        
        # run the method
        issues=gaw.get_issues(repository_full_name=repo_full_name)
        
        # test case is true when the number of the issues from the method is same as the test_issues 
        self.assertTrue(test_issues['open_issues']==issues['open_issues'] and test_issues['closed_issues']==issues['closed_issues'])


# test case to check the method can get the files of a selected repository
    def test_get_files(self):
        with open(os.getcwd() + "/.env", "r") as f:
            token = f.read().split("=")[1].strip()
        gaw = GithubAPIWrapper(token)
        
        # you can change the full repository name and the file list here
        
        full_repo_name = "morph3/crawpy"
        test_files = [  '.gitignore', 'README.md', 'common.txt', 'crawpy.py', 'reports/template.html',
                        'requirements.txt', 'src/Banner.py', 'src/RequestEngine.py', 'src/__init__.py', 'src/config.py']
        
        files=gaw.get_files(repository_full_name=full_repo_name)
        
        # test is true when the result of the method is same as the test_files
        self.assertTrue(files[i]['name']==test_files[i] for i in range(len(test_files)))





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
