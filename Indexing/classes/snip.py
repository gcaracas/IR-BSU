from collections import Counter
import math
import logging
import sys
sys.path.append("classes")
from classes.preprocessing import preprocessing
import operator
from classes.inverted_index import *
from classes.ranking import ranking
from tqdm import tqdm
import collections
import nltk

class snip:
    """
    Class to handle generating snippets operations.
    """
    def __init__(self):
        self.preproc = preprocessing()
        pass
    
    def get_snippets(self, ranked_results, resources=[], query="", i_i={}):
        sent_split = nltk.data.load('tokenizers/punkt/english.pickle')
        json_frontend = []

        for id, weight in tqdm(ranked_results):
            doc_id = resources[id]           
            original = i_i.storage.get(doc_id)['content']
            title, *text = original.split('\n\n')
            text = ' '.join(text)
            sentences = sent_split.tokenize(text)
            
            doc_snippet = self.gen_snip(document=sentences, query=self.preproc.the_works(query))

            json_frontend.append({'title':title, 'snippet':doc_snippet})
            
        return json_frontend
    
    def gen_snip(self, document=[], query=''):
        """
        :param sentence: String containing the sentence from the doc; this is a single string and it is not tokenized. 
        :param 
        
        :return: 
        """
        q_in_s = []
        print(document)
        print(query)

        proc_sents = []
        for s in document:
            proc_sents.append(self.preproc.the_works(s))
        for s in proc_sents:
            counter = 0
            for q in query:
                if q in s:
                    counter = s.count(q)
            q_in_s.append(counter)
        
        print(q_in_s)
        max_q_count = 0
        second_max_count = 0
        
        best_s_index = -1
        next_best_i = -1

        for s_index, q_count in enumerate(q_in_s):

            if q_count > max_q_count:
                second_max_count = max_q_count
                next_best_i = best_s_index

                max_q_count = q_count
                best_s_index = s_index

        snippet = str(document[best_s_index]) 
        snippet += "..." 
        snippet += str(document[next_best_i])

        return snippet




