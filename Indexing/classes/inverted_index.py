import numpy as np
import logging
import matplotlib.pyplot as plt
from tqdm import tqdm

from classes.preprocessing import preprocessing

class Appearance:
    """
    Represents the appearance of a term in a given document, along with the
    frequency of appearances in the same one.
    """

    def __init__(self, docId, frequency):
        self.docId = docId
        self.frequency = frequency


    def __repr__(self):
        """
        String representation of the Appearance object
        """
        return str(self.__dict__)


class inverted_index:

    def __init__(self, storage=''):
        logging.basicConfig(level=logging.INFO, format='%(filename)s %(levelname)s: %(asctime)s: %(message)s')
        self.logger = logging.getLogger('utils')
        self.index = {}
        self.storage = storage
        # Let's initialize our own preprocessing module
        self.preprocessing = preprocessing()
        self.preprocessing = preprocessing()
        # to visualize heaps law
        self.docs=[]
        self.unique_words=[]
        self.logger.info('Instantiating inverted index object')

    def __repr__(self):
        """
        String representation of the Database object
        """
        return str(self.index)

    def index_document(self, document='', process_text=True):
        """
        Process a given document, save it to the DB and update the index.
        """
        # Remove punctuation from the text.
        text = document['content']
        if process_text:
            text = self.preprocessing.remove_punctuation(text=text)

        # Tokenize
        tokens = self.preprocessing.tokenize(text=text)

        if process_text:
            # Remove stop words
            tokens = self.preprocessing.remove_stopwords(tokens=tokens)

            # Remove capitalization
            tokens = self.preprocessing.remove_capitalization(tokens=tokens)

            # Stem terms
            tokens = self.preprocessing.stem(tokens=tokens)

        appearances_dict = dict()
        # Dictionary with each term and the frequency it appears in the text.
        for term in tokens:
            term_frequency = appearances_dict[term].frequency if term in appearances_dict else 0
            appearances_dict[term] = Appearance(document['id'], term_frequency + 1)

        # Update the inverted index
        update_dict = {key: [appearance]
        if key not in self.index
        else self.index[key] + [appearance]
                       for (key, appearance) in appearances_dict.items()}
        self.index.update(update_dict)
        # Add the document into the database
        self.storage.add(document)
        return document

    def get_index_size(self):
        return len(self.index)

    def show_inverted_index(self):
        print(self.index)
        words=list(self.index.keys())
        print("{: >10} {: >10} {: >10} {: >10}".format("Id", 'Term', 'Document', 'Frequency'))
        print('{}'.format('-'*43))
        for id, word in enumerate(words):
            docs = [str(a.docId) for a in self.index[word]]
            docs_str = (str(d) for d in docs)
            docs_flat_list=','.join(docs_str)

            freq = [a.frequency for a in self.index[word]]
            freq_str = (str(d) for d in freq)
            freq_flat_list = ','.join(freq_str)
            print("{: >10} {: >10} {: >10} {: >10}".format(id,word,docs_flat_list, freq_flat_list))
    def lookup_query(self, query):
        """
        Returns the dictionary of terms with their correspondent Appearances.
        This is a very naive search since it will just split the terms and show
        the documents where they appear.
        """
        return {term: self.index[term] for term in query.split(' ') if term in self.index}

    def create_term_document_matrix(self, relevant_results={}):
        terms = list(self.index.keys())
        stemmed_tokens=[]
        for id, document in relevant_results.items():
            text = self.preprocessing.remove_punctuation(text=document['content'])
            tokens = self.preprocessing.tokenize(text=text)
            tokens = self.preprocessing.remove_stopwords(tokens=tokens)
            tokens = self.preprocessing.remove_capitalization(tokens=tokens)
            stems = self.preprocessing.stem(tokens=tokens)
            for stem in stems:
                found = False
                for token in tokens:
                    if token == stem:
                        found = True
                if found == False:
                    stemmed_tokens.append(stem)
        # We have now all the stemmed words that didn't match documents, now
        # let's make a unique list of them.
        stem_tokens = list(set(stemmed_tokens))

        # Now let's generate the matrix
        self.doc_term_matrix_all=[]
        for id, document in self.storage.index.items():
            term_doc_matrix=dict()
            text = self.preprocessing.remove_punctuation(text=document['text'])
            tokens = self.preprocessing.tokenize(text=text)
            tokens = self.preprocessing.remove_stopwords(tokens=tokens)
            tokens = self.preprocessing.remove_capitalization(tokens=tokens)
            stems = self.preprocessing.stem(tokens=tokens)
            for full_stem in stem_tokens:
                found = False
                for doc_stemmed_token in stems:
                    if full_stem == doc_stemmed_token:
                        found = True
                if found == True:
                    term_doc_matrix[full_stem] = 1
                else:
                    term_doc_matrix[full_stem] = 0
            self.doc_term_matrix_all.append(term_doc_matrix)

    def print_term_document_matrix(self):
        numeric_result_table=[]
        print(len(self.doc_term_matrix_all))
        terms = list(self.doc_term_matrix_all[0].keys())
        print(terms)
        title=['Terms/Document']
        for i in range(len(self.doc_term_matrix_all)):
            title.append('Doc {}'.format(i+1))
        print("{: >10} {: >10} {: >10} {: >10} {: >10} {: >10}".format(*title))
        for i in range(len(terms)):
            numeric_values=[]
            doc1 = self.doc_term_matrix_all[0][terms[i]]
            doc2 = self.doc_term_matrix_all[1][terms[i]]
            doc3 = self.doc_term_matrix_all[2][terms[i]]
            doc4 = self.doc_term_matrix_all[3][terms[i]]
            doc5 = self.doc_term_matrix_all[4][terms[i]]
            numeric_values.append(doc1)
            numeric_values.append(doc2)
            numeric_values.append(doc3)
            numeric_values.append(doc4)
            numeric_values.append(doc5)
            print('{: >10} {: >10} {: >10} {: >10} {: >10} {: >10}'.format(terms[i],
                                                                           doc1,
                                                                           doc2,
                                                                           doc3,
                                                                           doc4,
                                                                           doc5))
            numeric_result_table.append(numeric_values)
        self.numeric_term_doc=np.array(numeric_result_table)
    def term_term_correlation_matrix(self):
        self.numeric_term_term = np.matmul(self.numeric_term_doc, self.numeric_term_doc.transpose())
        for row in self.numeric_term_term:
            print(row)

    def create_index(self, collection=[],
                     process_text=False):
        self.logger.debug('Collection length = {}'.format(len(collection)))
        for i, doc in tqdm(enumerate(collection)):
            self.index_document(document=doc,
                               process_text=process_text)

    def visualize_freq(self):
        plt.figure(figsize=(6, 4), dpi=70)
        plt.loglog(self.docs, self.unique_words, marker=".")
        plt.title("Docs/Unique tokens")
        plt.xlabel("Documents")
        plt.ylabel("Unique words")
        plt.grid(True)
        plt.savefig('fig.png')
