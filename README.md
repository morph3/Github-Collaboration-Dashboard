# Github-Collaboration-Dashboard-Project 

This is the graduation project of the course CNG491 and CNG492. 

We are trying to develop a dashboard that visualizes and generates some metrics about Github repositories or users queried. Our goal is monitoring and making assumptions on how healthy a repository is.


# Requirements

In order to run or to make contributions to this project you need to install the python dependencides. You can install them by using the line below. (Make sure you are in the root of the folder).

```
pip install -r requirements.txt
```

or

```
python3 -m pip install -r requirements.txt
```


# Getting a personal token

Visit the url below, generate a new token. You can select the scopes you want to use, selecting all the ones with scope "read" should be enough for now.
```
https://github.com/settings/tokens/new
```

Your generated token should look like below
```
ghp_***********
```


Create a file named `.env` and put the the generated token into it like below,

```
GITHUB_TOKEN=ghp_***********
```

# Running

You can run the following command to run the application.
```
python3 app.py
```
# How to make a contribution

Create a new branch & a PR followingly.

To check all branches,you can use git's `branch` command in your command prompt:

```
git branch
```

The output should be like this:

```
C:\...\CNG491-Github-Collaboration-Dashboard>git branch
  dev
* main
...
```
The branch has an asterisk "`*`" in the beginning shows which branch are you working in right now. 

## Changing branch

In order to change branches in your local, you can use git's `checkout` function like this:

```
git checkout <branch_name>
```

# Authors  

Emir Ekin ÖRS  
Gizem ÜNDER  
Melih Kaan YILDIZ  
Sedat Ali ZEVİT 

## License
[MIT License](https://choosealicense.com/licenses/mit/)
