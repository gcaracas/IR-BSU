import logging
from classes.utilities import doc_utilities
from classes.persist_index_memory import persist_index_memory
from classes.inverted_index import inverted_index
from classes.ranking import ranking
from classes.preprocessing import preprocessing



logging.basicConfig(level=logging.DEBUG, format='%(filename)s %(levelname)s: %(asctime)s: %(message)s')
logger = logging.getLogger('main')
logger.info('Executing indexing module')
logger.info('Reading file')
u = doc_utilities()
u.read_data_set(file='data/wikipedia_text_files.csv', docs=50)
memory_unit = persist_index_memory()
u.process_documents_for_indexing()
i_i = inverted_index(memory_unit)
i_i.create_index(collection=u.get_collection_json(),
                     process_text=True)
i_i.create_term_document_matrix()
r_ranking = ranking()
max_freq = r_ranking.get_max_frequencies(index=i_i.index, num_docs=len(i_i.storage.index))
# Now save this into the persisted memory object within the index
i_i.storage.max_frequency_terms_per_doc = max_freq
res = r_ranking.relevance_ranking(query = 'state nation disput local employ the',
                           num_results=5,
                            index=i_i.index,
                            resources=[1, 2, 3, 4, 5, 8, 23, 44],
                            max_freq=i_i.storage.max_frequency_terms_per_doc,
                            N=len(i_i.storage.index),
                            term_doc_matrix=i_i.doc_term_matrix_all)
print(res)

