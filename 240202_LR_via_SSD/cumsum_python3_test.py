# numpy style cumsum in Python 3+ onwards
"""
# REFER: https://www.geeksforgeeks.org/python-program-to-find-cumulative-sum-of-a-list/
from itertools import accumulate           # itertools accumulate is only available in Python 3+
import operator

def cumulative_sum(input_list):
    # cumulative_sum
    # Use the accumulate() function to perform a cumulative sum of the elements in the list
    cumulative_sum_iter = accumulate(input_list, operator.add)
    # Convert the iterator to a list and return it
    return list(cumulative_sum_iter)
"""