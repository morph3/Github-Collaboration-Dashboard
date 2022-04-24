import json
from datetime import datetime
class SimpleStorage:
    def __init__(self):
        """
        With the functionalities added, it is hard to call it cache utility anymore, now it is data storage.
        """
        self.size       = 0 # set the site to be 0 initially
        self.storage    = [] # this is a list of dictionaries, this can be changed into further use later on but we are using array of dictionaries now.
        self.filename   = "storage.json" # default

    def load_file(self, filename):
        """
        Load the data from the file.
        """
        self.filename = filename
        with open(filename, "r") as f:
            self.storage = json.load(f)
        
        self.size = len(self.storage)
        self.sort()
    
        return
    
    def update_file(self):
        """
        Update the file with the current storage.
        """
        with open(self.filename, "w") as f:
            json.dump(self.storage, f, indent=4)
        return
    
    def add(self, data):
        """
        Add data to the storage. data is a dictionary.
        """
        self.storage.append(data)
        self.size = self.size + 1
        self.sort() # just to make sure
        self.update_file()
        return
    
    
    def get_all(self, repo_name, type):
        
        """
        Get the data(s) from the storage.
        
        For example, if storage.get_all("xct/ropstar","heuristic") is called, it will return every entry for the repository "xct/ropstar" with type "heuristic".
        """
        arr = []
        for i in self.storage:
            try:
                if (i["repository_name"] == repo_name) and (i["type"] == type):
                    arr.append(i)
            except:
                continue
        return arr
    
    
    def get_last(self, repo_name, type):
        """
        Returns the last element based on given info. If the given info does not exist, it will return False.
        """
        if self.size == 0:
            return False
        
        datas = self.get_all(repo_name, type)
        if len(datas) == 0:
            return False
        else:
            return datas[-1]


    def remove(self, date):
        """
        Remove the data with the given date from the storage. 
        
        Removing an entry is kind of hard as we have many keys in the dictionary. We can use the date as the key as it will be the most unique one.
        """
        for i in self.storage:
            if i["date"] == date:
                print(f"Removing entry from the storage:\n{item}")
                self.storage.remove(i)
                self.size = self.size - 1
        self.update_file()
        pass

    def sort(self):
        """
        Sort the data in the storage with date key.
        
        Sorting an array of dictionary is kind of hard as we have many keys in the dictionary. We can use the date as the key as it will be the most unique one.
        """
        self.storage.sort(key = lambda x: datetime.strptime(x["date"], "%Y-%m-%d %H:%M:%S"))

        pass
    


    def __str__(self):
        """
        Print the storage.
        """
        for i in self.storage:
            print(json.dumps(i, indent=4))
        print(f"Number of entries in the storage: {self.size}")
        return ""

