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

    def scale(self, CR, match_num=int):
        """
        Change the number of exact terms to match between query and resource
        """ 
        scaled = {k: CR[k] for k in CR if len(CR[k]) == match_num}
        return {k: CR[k] for k in CR if len(CR[k]) == match_num}
    
    def boolean(self, CR):
        """
        boolean matching strategy
        """
        matches = {}
        match_list = []
        for token in CR:
            for val in CR[token]:
                match = (str(token), val.docId, val.content_frequency, val.title_frequency) #val.docId,  
                match_list.append(match)
                if val.docId not in matches:
                    matches[val.docId] = [match] 
                else:
                    matches[val.docId].append(match)
        
        # 1. Find docs w/most different matching terms from query, 
        # to increase prob of meeting user info need         
        docToken_matchNums = [len(i) for i in matches.values()]
        scaler = max(docToken_matchNums)
        
        # while len(most_matching_terms) < 10 and scaler > 1:
        #     scaler -= 1
        #     next_most_mt = self.scale(matches, scaler)
        #     most_matching_terms.update(next_most_mt)
        resources = []
        if scaler > 1:
            most_matching_terms = self.scale(matches, scaler)
            list_most_matches = most_matching_terms.values()
            if len(list_most_matches) >= 5:
                for i in range(5):
                    resources.append(list_most_matches[i])
            else:
                for i in range(len(list_most_matches)):
                    resources.append(list_most_matches[i])

        # resources = list(most_matching_terms.values())    
        # 2. prioritize docs w/the most matching terms...
        #... in the title ...
        title_sum = sorted(match_list, key=lambda x: x[3], reverse=True)[0:20]

        #... and in the text
        content_sum = sorted(title_sum, key=lambda x: x[2], reverse=True)[0:10]

        resources.extend(content_sum)
        rsrcs = [i[1] for i in resources]

        return rsrcs 