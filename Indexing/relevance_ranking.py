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
                     process_text=True)
i_i.create_term_document_matrix()

# GIVEN QUERY FROM FRONT-END, FIND RELEVANT RESULTS
query = 'Duck' # user input
print('input:',query)
matcher = match()
q = preprocessing().the_works(query)
# print('processed query', q)
CR = i_i.lookup_query(q)
# print('worked 1st?',len(CR['duck']))
CR = matcher.boolean(CR)
# print('worked 2nd?',len(CR))
# added in case not every token matches
doctoken_matchnums =[len(i) for i in CR.values()]
scaler = max(doctoken_matchnums)
# print('worked 3rd?',len(CR))
CR = matcher.scale(CR,scaler)
# print('still there? ',CR.keys(), CR.values())
# for key in CR:
#     print(CR[key])

# RANK RELEVANT RESULTS
r_ranking = ranking()
resources = list(CR.keys())
# print('resources: ', resources)

max_freq = [r_ranking.get_highest_frequency(i_i, r) for r in resources]

# max_freq = r_ranking.get_max_frequencies(index=CR) # , num_docs=len(i_i.storage.index)

# Now save this into the persisted memory object within the index
print(max_freq)

i_i.storage.max_frequency_terms_per_doc = max_freq
print('***************************************************')
res = r_ranking.relevance_ranking(query = query,
                           num_results=5,
                            index=i_i.index,
                            resources=resources,
                            max_freq=i_i.storage.max_frequency_terms_per_doc,
                            N=len(i_i.storage.index),
                            term_doc_matrix=i_i.doc_term_matrix_all,
                            weigh=False,
                            query_weighing=False,
                            CR=CR)

print(res)
print('**************************************************')
# GENERATE RANKED JSON_SNIPPETS FOR FRONT-END
snipper = snip(r_ranking)
json = snipper.get_snippets(res, resources=resources, query=query, i_i=i_i)

print('output:',json)
