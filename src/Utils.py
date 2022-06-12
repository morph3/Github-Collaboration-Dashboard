
import numpy as np
from pygini import gini

"""
This is the file that holds the utility functions
"""

def calculate_gini_index(data):
    """
    Calculate the gini index of the data
    """
    # take the absolute value of the data
    data = np.array(data, dtype=float)
    
    # uncomment the following line if you want to see the values of the data
    #print(data)
    
    # return the gini index of the data
    return gini(data)

def dot_env_parser():
    env = {}
    f = open(".env","r").read()
    for line in f.splitlines():
        k, v = line.split("=")
        env[k] = v
    return env

def generate_random_datetime(n, start_date="-90d", end_date="now"):
    # if this is called, import Faker library
    from faker import Faker
    """
    >>> for i in range(100):
    ...     f.date_time_between(start_date="-90d", end_date="now").strftime('%Y-%m-%d %H:%M:%S')
    ...
    '2022-03-12 19:17:26'
    '2022-04-03 18:27:14'
    '2022-01-29 21:13:55'
    '2022-03-17 12:27:41'
    '2022-04-07 14:47:20'
    '2022-04-15 17:06:56'
    '2022-02-05 07:57:59'
    '2022-03-13 02:22:00'
    '2022-02-09 18:42:26'
    '2022-03-13 11:18:08'
    '2022-02-12 21:41:24'
    '2022-01-28 06:35:14'
    """

    f = Faker()
    dates = []
    for i in range(n):
        dates.append(f.date_time_between(start_date="-90d", end_date="now").strftime('%Y-%m-%d %H:%M:%S'))
    return dates

