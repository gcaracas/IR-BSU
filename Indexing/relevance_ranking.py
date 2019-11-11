import logging
from classes.utilities import doc_utilities
from classes.persist_index_memory import persist_index_memory
from classes.inverted_index import inverted_index
from classes.ranking import ranking
from classes.preprocessing import preprocessing
from classes.snip import snip
from classes.match import match
import nltk

logging.basicConfig(level=logging.DEBUG, format='%(filename)s %(levelname)s: %(asctime)s: %(message)s')
logger = logging.getLogger('main')
logger.info('Executing indexing module')
logger.info('Reading file')

# LOAD DATASET
u = doc_utilities()
u.read_data_set(file='data/12000_docs.p')
memory_unit = persist_index_memory()
u.process_documents_for_indexing()
i_i = inverted_index(memory_unit)

# CREATE INDEX FROM DATASET

i_i.create_index(collection=u.get_collection_json(),
                     process_text=True, 
                     max_tokens=100000)
i_i.create_term_document_matrix()

# GIVEN QUERY FROM FRONT-END, FIND RELEVANT RESULTS
query = 'duck tales' # user input
print('\n**************\ninput:',query)

matcher = match()
q = preprocessing().the_works(query)
print('\n*******what have you done to my beautiful query?\n', q)
CR = i_i.lookup_query(q)

resources = matcher.boolean(CR)
print("after matching", resources)

# RANK RELEVANT RESULTS
r_ranking = ranking()
max_freq = r_ranking.get_max_frequencies(index=i_i.index) # sentence_tokens=q, num_docs=len(i_i.storage.index)
# Now save this into the persisted memory object within the index
i_i.storage.max_frequency_terms_per_doc = max_freq
res = r_ranking.relevance_ranking(query = query,
                           num_results=5,
                            index=i_i.index,
                            resources=resources,
                            max_freq=i_i.storage.max_frequency_terms_per_doc,
                            N=len(i_i.storage.index),
                            term_doc_matrix=i_i.doc_term_matrix_all)

print(res)
# GENERATE RANKED JSON_SNIPPETS FOR FRONT-END
snipper = snip()
json = snipper.get_snippets(res, resources=resources, query=query, i_i=i_i)

print('output:',json)
