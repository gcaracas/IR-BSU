# This script loads the index in memory and returns the objects, from
# which we will reuse them.
import logging
import sys
# **************************************
# * IPORTANT NOTE IN RELATIVE PATH  ****
# **************************************
# This script is called by applicaiton.py
# that lives inside the App directory,
# thus all relative paths on this file
# assumes application.py was the caller,
# therefore the path.appends start at
# the /App level.
sys.path.append("classes")
from utilities import doc_utilities
from persist_index_memory import persist_index_memory
from inverted_index import inverted_index



class load_index_in_memory:
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG, format='%(filename)s %(levelname)s: %(asctime)s: %(message)s')
        self.logger = logging.getLogger('load_in_memory')

    def load_index(self):
        self.logger.info('[Load index 1/8] Loading index in memory')

        # Reading collection
        self.logger.info('[Load index 2/8] Reading document')
        u = doc_utilities()
        u.read_data_set(file='../Indexing/data/wikipedia_text_files.csv', docs=100000)

        # Create memory unit that will hold
        # the full collection
        self.logger.info('[Load index 3/8] Instantiating index in memory')
        memory_unit = persist_index_memory()

        # Prepare documents for indexing
        self.logger.info('[Load index 4/8] Preparing document for indexing')
        u.process_documents_for_indexing()

        # Start indexing
        self.logger.info('[Load index 5/8] Creating inverted index')
        i_i = inverted_index(memory_unit)
        self.logger.info('[Load index 6/8] Creating main index')
        i_i.create_index(collection=u.get_collection_json(),
                        process_text=True,
                        max_tokens=100000)
        self.logger.info('[Load index 7/8] Creating term-document matrix')
        i_i.create_term_document_matrix()
        self.logger.info('[Load index 8/8] Preloading index done')
        return i_i, memory_unit