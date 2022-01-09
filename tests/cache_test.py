import json
import os
TRUCK_FACTOR_CACHE = ""
CACHE_FILE = None
CACHE_NAME = "cache.json"

def check_cache(repo_name, type):
    # if the cache is empty return None
    if TRUCK_FACTOR_CACHE == "":
        return None

    # if the item is in the cache, return it
    for item in TRUCK_FACTOR_CACHE:
        try:
            if (item["repository_name"] == repo_name) and (item["type"] == type):
                return item
        except:
            continue
    return None

def update_cache(entry):

    # if the cache is empty    
    if TRUCK_FACTOR_CACHE == "":
        CACHE_FILE = open(CACHE_NAME, "w")
        CACHE_FILE.write(entry)
        CACHE_FILE.close()
    
    TRUCK_FACTOR_CACHE.append(entry)
    CACHE_FILE = open(CACHE_NAME, "w")
    CACHE_FILE.write(json.dumps(TRUCK_FACTOR_CACHE))
    CACHE_FILE.close()
    
def display_cache():
    
    print(TRUCK_FACTOR_CACHE)


if __name__ == "__main__":
        # if the cache.json file exists, load it
    if os.path.exists(CACHE_NAME):
        CACHE_FILE = open(CACHE_NAME,"r") # array of json objects 
        TRUCK_FACTOR_CACHE = json.loads(CACHE_FILE.read())
        CACHE_FILE.close()
    
    update_cache({"repository_name": "xct/ropstar", "type": "commit", "users": ["xct"], "truck_factor": 1})
    display_cache()