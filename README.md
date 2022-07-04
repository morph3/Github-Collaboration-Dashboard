# Github Collaboration Dashboard 

This is our university graduation project. Related courses are `CNG491` and `CNG492` of `Middle East Technical University Northern Cyprus Campus` .

Supervised by Dr. Sukru Eraslan.

## Introduction

We are trying to develop a dashboard that visualizes and generates some metrics about Github repositories or users queried. Our goal is monitoring and making assumptions on how healthy a repository is by looking at various indicators.


## Requirements

You can install the requirements as follows,

```
pip install -r requirements.txt
```

Additionally, a github personal token is needed to run the application.

Visit the url below, generate a new token. You can select the scopes you want to use, selecting all the ones with scope "read" should be enough for now.

```
https://github.com/settings/tokens/new
```


Create a file named `.env` and put the the generated token in it like below,

```
GITHUB_TOKEN=ghp_***********
```

## Running

You can run the following command to run the application.
```
python3 app.py
```

## Examples

Repository based searches,

![](https://i.imgur.com/Pvq9aOG.png)

Charts section of repository based searches,

![](https://i.imgur.com/8no7acQ.png)

User based searches,
![](https://i.imgur.com/G9bFas5.png)


## Authors  

Emir Ekin ÖRS  
Gizem ÜNDER  
Melih Kaan YILDIZ  
Sedat Ali ZEVİT 

## License
[MIT License](https://choosealicense.com/licenses/mit/)

## References

https://doi.org/10.1109/ICPC.2017.35  
https://doi.org/10.1145/2884781.2884851   
https://doi.org/10.1109/ICPC.2016.7503718   
https://doi.org/10.1109/SANER.2015.7081864    
https://www.sciencedirect.com/science/article/abs/pii/S0164121220300911   

