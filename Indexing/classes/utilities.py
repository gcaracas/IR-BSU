import logging
import pickle
import pandas as pd

class doc_utilities:
    def __init__(self):
        logging.basicConfig(format='%(filename)s %(levelname)s: %(asctime)s: %(message)s')
        self.logger = logging.getLogger('utils')
        self.collection = ''

    def read_data_set(self, file=''):
        if len(file) == 0: self.logger.error("file parameter missing")
        collection = pickle.load(open("{}".format(file), "rb"))
        self.collection = collection.rename(columns={"content": "text",
                                                     "title": "title",
                                                     "id": "id"})

    # this is an abstraction layer, this could be changed to a db query, however the main
    # caller won't notice that, as long as the method name and parameters are the same.
    def get_number_documents(self):
        return self.collection.shape[0]

    def process_documents_for_indexing(self):
        self.logger.info('Converting document to be ready to be indexed')
        self.json_collection=self.collection.to_dict('records')

    def get_collection_json(self):
        return self.json_collection
