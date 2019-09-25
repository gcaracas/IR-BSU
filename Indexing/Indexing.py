import pickle
import logging
from classes.utilities import doc_utilities
from classes.persist_index_memory import persist_index_memory
from classes.inverted_index import inverted_index
from tqdm import tqdm


logging.basicConfig(level=logging.DEBUG, format='%(filename)s %(levelname)s: %(asctime)s: %(message)s')
logger = logging.getLogger('main')


def main():
    logger.info('Executing indexing module')
    logger.info('Reading file')
    u = doc_utilities()
    u.read_data_set(file='data/data-1000.pk')
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

    # Now let's index our collection
    with tqdm(total=len(u.get_collection_json()), desc="Indexing documents", bar_format="{l_bar}{bar} [ time left: {remaining} ]") as pbar:
        for doc in u.get_collection_json():
            i_i.index_document(document=doc,
                               preprocessing=False)
            pbar.update(1)

    logger.info('Task 2, Index size without preprocessing = {}'.format(i_i.get_index_size()))

    # Now let's recreate everything and now let's preprocess.
    memory_unit = persist_index_memory()
    u.process_documents_for_indexing()
    i_i = inverted_index(memory_unit)
    with tqdm(total=len(u.get_collection_json()), desc="Indexing documents",
              bar_format="{l_bar}{bar} [ time left: {remaining} ]") as pbar:
        for doc in u.get_collection_json():
            i_i.index_document(document=doc,
                               preprocessing=True)
            pbar.update(1)
    logger.info('Task e, Index size with preprocessing = {}'.format(i_i.get_index_size()))






if __name__ == "__main__":
    main()
