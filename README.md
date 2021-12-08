# CNG491-Github-Collaboration-Dashboard

# Introduction

This is the graduation project of the course CNG491 and CNG492. 


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



# Authors  

Emin Ekin ÖRS  
Gizem ÜNDER  
Melih Kaan YILDIZ  
Sedat Ali ZEVİT 

## License
[MIT License](https://choosealicense.com/licenses/mit/)
