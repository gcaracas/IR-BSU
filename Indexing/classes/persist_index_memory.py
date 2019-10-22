import logging

class persist_index_memory:
    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='%(filename)s %(levelname)s: %(asctime)s: %(message)s')
        self.logger = logging.getLogger('utils')
        self.index = {}
        self.logger.info('Instantiating storage object')
        self.max_frequency_terms_per_doc = []
    def __repr__(self):
        """
        String representation of the Database object
        """
        return str(self.__dict__)

    def get(self, id):
        return self.index.get(id, None)

    def add(self, document):
        return self.index.update({document['id']: document})

    def remove(self, document):
        return self.index.pop(document['id'], None)
