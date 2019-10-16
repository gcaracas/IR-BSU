import logging
import sys
#sys.path.insert(0, '/Users/jason.smith/Documents/GitHub/IR-BSU/Indexing/classes')
sys.path.append("../Indexing/classes")
from ranking import ranking
from preprocessing import preprocessing
from snip import snip
from match import match

def search(query1, i_i):
    logging.basicConfig(level=logging.DEBUG, format='%(filename)s %(levelname)s: %(asctime)s: %(message)s')
    logger = logging.getLogger('main')
    logger.info('Executing indexing module')
    logger.info('Reading file')
    # GIVEN QUERY FROM FRONT-END, FIND RELEVANT RESULTS
    query =  query1# user input
    print('input:',query)
    matcher = match()
    q = preprocessing().the_works(query)
    CR = i_i.lookup_query(q)
    CR = matcher.boolean(CR)
    # added in case not every token matches
    doctoken_matchnums =[len(i) for i in CR.values()]
    if len(doctoken_matchnums) == 0: return ''
    scaler = max(doctoken_matchnums)
    CR = matcher.scale(CR,scaler)

    # RANK RELEVANT RESULTS
    r_ranking = ranking()
    resources = list(CR.keys())
    max_freq = r_ranking.get_max_frequencies(index=CR) # , num_docs=len(i_i.storage.index)
    # Now save this into the persisted memory object within the index
    i_i.storage.max_frequency_terms_per_doc = max_freq
    res = r_ranking.relevance_ranking(query = query,
                               num_results=5,
                                index=i_i.index,
                                resources=resources,
                                max_freq=i_i.storage.max_frequency_terms_per_doc,
                                N=len(i_i.storage.index),
                                term_doc_matrix=i_i.doc_term_matrix_all)

    # GENERATE RANKED JSON_SNIPPETS FOR FRONT-END
    snipper = snip(r_ranking)
    json = snipper.get_snippets(res, resources=resources, query=query, i_i=i_i)

    # print('output:',json)
    return(json)
