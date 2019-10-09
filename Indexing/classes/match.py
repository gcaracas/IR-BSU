from collections import Counter
import math
import logging
from classes.preprocessing import preprocessing
import operator
from classes.inverted_index import *
from classes.ranking import ranking
from tqdm import tqdm
import collections

class match:
    """
    Class to handle matching query to relevant resources.
    """
    def __init__(self):
        pass

    def scale(self, CR={}, match_num=int):
        """
        Change the number of exact terms to match between query and resource
        """
        return {k: CR[k] for k in CR if len(CR[k]) == match_num}
    
    def boolean(self, CR):
        """
        boolean matching strategy
        """
        doc_first = {}
        len_DC=1699999
        # better way of generating pertinent indices?
        for i in range(1, len_DC+1):
            doc_first[i] = []    

        for token in CR:
            for val in CR[token]:
                match = ('match: ' + str(token), val.frequency)
                doc_first[val.docId].append(match)
        return {k: doc_first[k] for k in doc_first if len(doc_first[k]) > 0}
    



