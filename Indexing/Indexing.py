import pickle
import logging
from classes.utilities import doc_utilities
from classes.persist_index_memory import persist_index_memory
from classes.inverted_index import inverted_index
from tqdm import tqdm
import pandas as pd


logging.basicConfig(level=logging.DEBUG, format='%(filename)s %(levelname)s: %(asctime)s: %(message)s')
logger = logging.getLogger('main')

def main():
    logger.info('Executing indexing module')
    logger.info('Reading file')
    u = doc_utilities()
    u.read_data_set(file='data/wikipedia_text_files.csv', docs=12700)
    #u.read_data_set(file='data/wikipedia_text_files.csv', docs=120)
    logger.info('Task1 - Number of documents = {}'.format(u.get_number_documents()))

    # Instantiate our presistent object
    memory_unit = persist_index_memory()

    # Files can be in any format, let's convert them into a
    # json array, in this format:
    '''
    doc1 = {'id': 1, 'text': txt1}
    doc2 = {'id': 2, 'text': txt2
    doc3 = {'id': 3, 'text': txt3}
    doc4 = {'id': 4, 'text': txt4}
    doc5 = {'id': 5, 'text': txt5}
    '''
    u.process_documents_for_indexing()

    # Now let's instantiate our inverted index code
    i_i = inverted_index(memory_unit)

    # Let's transform our collection as an array of
    # JSON elements.
    #u.process_documents_for_indexing()

    # Now let's create our index
    i_i.create_index(collection=u.get_collection_json(),
                     preprocessing_text=False)
    logger.info('Index size = {}'.format(i_i.get_index_size()))

    r=i_i.lookup_query('man')
    print(r)
    logger.info('Done Indexing')


if __name__ == "__main__":
    main()
