from collections import Counter
import math
import logging
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
    def __init__(self, ranker=''):
        self.preproc = preprocessing()
        self.ranker = ranker
        pass

    
    def cos_similarity(self, d_weights, q_weights):
        """
        calculate cosine similarity between 2 vectors (lists of numbers)
        For snippet generation
        """
        numerator = sum([d*q for d,q in zip(d_weights, q_weights)])
        d_norm = sum([d*d for d in d_weights])
        q_norm = sum([q*q for q in q_weights])
        denom = np.sqrt(d_norm * q_norm)
        return numerator/denom
    
    def get_snippets(self, ranked_results, resources=[], query="", i_i={}):
        
        #print('get_snippets called')
        sent_split = nltk.data.load('tokenizers/punkt/english.pickle')
        json_frontend = []

        for id, weight in tqdm(ranked_results):
         #   print('id', id)
            doc_id = resources[id]
          #  print('doc id found')
            # retrieve original unprocessed doc-string    
            original = i_i.storage.get(doc_id)['content']
           # print('doc retrieved from i_i\'s stroage')
            # get doc title
            title, *text = original.split('\n\n')
            text = ' '.join(text)

            # separate text into sentences
            sentences = sent_split.tokenize(text)

         #   print('before gen snip call', id)
            # generate snippet
            doc_snippet = self.gen_snip(document=sentences, i_i=i_i, query=query)

            # prepare for frontend
            json_frontend.append({'title':title,     'snippet':'...'.join(doc_snippet)})
            
          #  print('title', title, 'snippet','...'.join(doc_snippet))
            
        return json_frontend
    
    def gen_snip(self, document=[], i_i={}, query=''):
        """
        :param sentence: String containing the sentence from the doc; this is a single string and it is not tokenized. 
        :param 
        
        :return: 
        """
        # derive weights for tokens in query
        q = self.preproc.the_works(query)
        q_max_freqs = self.ranker.get_max_frequencies(index=i_i.index, sentence_tokens=q)
        i_i.storage.max_frequency_terms_per_doc = q_max_freqs
        
        q_weights=self.ranker.relevance_ranking(query = query,
                           num_results=len(q),
                            index=i_i.index,
                            resources=[],
                            max_freq=i_i.storage.max_frequency_terms_per_doc,
                            N=len(i_i.storage.index),
                            term_doc_matrix=i_i.doc_term_matrix_all,
                            weigh=True,
                            query_weighing=True)   
        q_w=[w[1] for w in sorted(q_weights, key=lambda x: x[0])]
            
        print('num results for q_weights', query)
        print('query weights generated', q_w)
        cos_score = -1.0
        
        # save only the 2 closest sentences
        snippet = collections.deque(maxlen=2)

        # derive weights for sentences in document...
        for i in range(len(document)):
            s = document[i]
            s_max_freqs = self.ranker.get_max_frequencies(index=i_i.index, sentence_tokens=self.preproc.the_works(text=s))
            i_i.storage.max_frequency_terms_per_doc = s_max_freqs
            #print('num_results for s_weights',s)

            s_weights = self.ranker.relevance_ranking(query = s,
                                   num_results=len(s),
                                    index=i_i.index,
                                    resources=[], 
                                    max_freq=i_i.storage.max_frequency_terms_per_doc,
                                    N=len(i_i.storage.index),
                                    term_doc_matrix=i_i.doc_term_matrix_all,
                                    weigh=True)

            ordered_s_weights = [w[1] for w in sorted(s_weights, key=lambda x: x[0])]
            #print('weighted words',ordered_s_weights)

            #print('doc weights generated', ordered_s_weights)
            cosine_sim = self.cos_similarity(ordered_s_weights, q_w)

            print('cosine score', cosine_sim)

            #print('cosine similarity calculated', cosine_sim)
            if cosine_sim > cos_score:
                cos_score = cosine_sim
                snippet.append(s)
        return snippet




