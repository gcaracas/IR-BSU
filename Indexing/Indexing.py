import pickle
import logging
from classes.utilities import doc_utilities
from classes.persist_index_memory import persist_index_memory
from classes.inverted_index import inverted_index
from tqdm import tqdm
import pandas as pd


logging.basicConfig(level=logging.DEBUG, format='%(filename)s %(levelname)s: %(asctime)s: %(message)s')
logger = logging.getLogger('main')
max_unique_words_index = 100000

def main():
    logger.info('Executing indexing module')
    logger.info('Reading file')
    u = doc_utilities()
    #u.read_data_set(file='data/data-1000.pk')
    u.read_data_set(file='data/wikipedia_text_files.csv')
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
    u.process_documents_for_indexing()

    # Now let's create our index
    i_i.create_index(collection=u.get_collection_json(),
                     preprocessing_text=False,
                     max_unique_words=max_unique_words_index)

    i_i.visualize_freq()

    # Now let's index our collection
    #with tqdm(total=len(u.get_collection_json()), desc="Indexing documents", bar_format="{l_bar}{bar} [ time left: {remaining} ]") as pbar:
    #    for doc in u.get_collection_json():
    #        i_i.index_document(document=doc,
    #                           preprocessing=False)
    #        pbar.update(1)

    #logger.info('Task 2, Index size without preprocessing = {}'.format(i_i.get_index_size()))

    # Now let's recreate everything and now let's preprocess.
    #memory_unit = persist_index_memory()
    #u.process_documents_for_indexing()
    #i_i = inverted_index(memory_unit)
    total_unique_words_sofar=0
    #with tqdm(total=max_unique_words_index, desc="Indexing documents",
    #          bar_format="{l_bar}{bar} [ time left: {remaining} ]") as pbar:
    #for doc in u.get_collection_json():
    #    i_i.index_document(document=doc,
    #                        preprocessing=False)
    #    #pbar.update(i_i.get_index_size() - total_unique_words_sofar)
    #    total_unique_words_sofar = i_i.get_index_size()
    #    percentage=(total_unique_words_sofar/max_unique_words_index)*100
    #    logger.debug('Doc indexed so far = %{}'.format(percentage))
    #    if total_unique_words_sofar >= max_unique_words_index:
    #       break;

    logger.info('Done Indexing')


if __name__ == "__main__":
    main()
