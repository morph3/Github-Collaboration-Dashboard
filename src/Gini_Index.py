
import numpy as np
from pygini import gini


def calculate_gini_index(data):
    """
    Calculate the gini index of the data
    """
    data = np.array(data, dtype=float)
    print(data)
    return gini(data)


if __name__ == '__main__':
    "For test purposes"
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print(calculate_gini_index(data))
    data = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    print(calculate_gini_index(data))
    data=[1]
    print(calculate_gini_index(data))
