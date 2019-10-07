from collections import Counter
import math
import logging
from classes.preprocessing import preprocessing
import operator
from classes.inverted_index import *
from tqdm import tqdm


class ranking:
    """
    Class to handle ranking operations.
    """
    def __init__(self):
        pass

    def get_term_frequency(self, entries={}, doc_id=0):
        """
        Using our inverted index to get our data, we will
        :param entries: all indexed terms frequency in that document
        :param doc_id: id of that document to process
        :return:
        """
        # Iterate through all the documents where this term occurs:
        for elem in entries:
            if int(elem.docId) == doc_id:
                # Return immediately, this is an expensive operation.
                return elem.frequency
        # Term not in that document
        return 0

    def get_highest_frequency(self, index={}, doc_id=0):
        """
        Calculates the max_subd, which is the number of times the most
        frequent-occurred term appears in d.
        :param index: index
        :param doc_id: the document we will process
        :return: the max frequency found.
        """
        tmp_freq = 0
        for key, val in index.items():
            # val is an array of docId, frequency objects
            # of the documents that key(term) occurs.
            
            # key is the docId
            # val is the matching term and its freq in the doc
            for elem in val:
                if key == doc_id: #if int(elem.docId) == doc_id:
                    if elem.frequency > tmp_freq:
                        tmp_freq = elem.frequency
        return tmp_freq

    def n_w(self, term_doc_matrix, term=''):
        num_docs=0.00001
        for d in term_doc_matrix:
            if term in d:
                num_docs = num_docs + d[term]
            else:
                continue
        return num_docs

    def relevance_ranking(self, query='', num_results=5, index=[], resources=[], max_freq=[], N=0, term_doc_matrix=[]):
        """
        Calculate relevance ranking
        :param query: String containing the query, this is a single string and it is not tokenize
        :param num_results: Integer, indicates the number of results returned by the ranking operation
        :param resources: Array of document id's that will be processed
        :return: Array of ranked documents.
        """
        logging.info("Performing ranking, query = {}, results = {}".format(query, num_results))

        # Now we will preprocess and tokenize our query.
        p = preprocessing()
        text = p.remove_punctuation(text=query)
        tokens = p.tokenize(text=text)
        tokens = p.stem(tokens=tokens)
        tokens = p.remove_stopwords(tokens=tokens)
        q = p.remove_capitalization(tokens=tokens)
        results={}

        # We will iterate through all the documents in the resources list
        for id in resources:
            TF=0
            IDF=0
            #Iterate through query tokens
            for w in q:
                if w not in index:
                    print('Term {} not found in index'.format(w))
                    continue
                freq = self.get_term_frequency(entries=index[w], doc_id=id)
                max_d = max_freq[id-1] #For base 0 reason
                # Now calculate TF
                TF = TF+freq/max_d
                # Now calculate IDF
                n_w=self.n_w(term_doc_matrix=term_doc_matrix, term=w)
                IDF = IDF+math.log2(N/n_w)
            # Now let's join the TF-IDF
            results[id] = TF*IDF
        sorted_result = sorted(results.items(), key=operator.itemgetter(1), reverse = True)
        return sorted_result[:num_results]

    def get_max_frequencies(self, index={}, num_docs=0):
        """
        Calculates the maximum frequency of any term in all documents, so we
        can use it in ranking.
        :param index: main index
        :param num_docs: Total number of documents
        :return: array from 1..n where n is num of documents, with the highest
        term frequency.
        """
        max_freq=[]
        
        for docId, matches in CR.items():
            tmp_freq = 0
            for token in matches:

                frequency = token[1]
                if frequency > tmp_freq:
                    print(token[0])
                    tmp_freq = frequency
                    print(tmp_freq)
        
        for document_id in tqdm(range(1,num_docs+1)):
            max_freq.append(self.get_highest_frequency(index=index, doc_id=document_id))

        return max_freq




