
from threading import Thread
# import Queue
import json
import multiprocessing
import time
import os, pickle
import pandas as pd
from datetime import datetime
from dateutil.parser import parse


# def find_sugg(query, file):
#     sugg = []
#     with open(file) as data_file:
#         data = json.load(data_file)
#     for l in data:
#         if (query in str(l['query'])):
#             sugg.append(str(l['query']))
#     exit(sugg)
#     # q.put(sugg)
#
# def score(cand):
#
# # number of total queries in aql = 3942354
#
# def qsIndex(file):
#
#     with open("AQL/Clean-Data-01.txt") as f:
#         for line in f:
#             line = line.strip().split("\t")
#             if (line[0] != "AnonID"):


if __name__ == '__main__':
    start_time = time.time()
    # q = "merit"
    # suggestions = []
    # jobs = []
    # que = Queue.Queue()
    # jobs.append(multiprocessing.Process(target=find_sugg, args=(q, 'AQL/aql1.json',)))
    # jobs.append(multiprocessing.Process(target=find_sugg, args=(q, 'AQL/aql2.json',)))
    # jobs.append(multiprocessing.Process(target=find_sugg, args=(q, 'AQL/aql3.json',)))
    # jobs.append(multiprocessing.Process(target=find_sugg, args=(q, 'AQL/aql4.json',)))
    # jobs.append(multiprocessing.Process(target=find_sugg, args=(q, 'AQL/aql5.json',)))
    #
    # for p in jobs:
    #     p.start()
    #
    # for p in jobs:
    #     p.join()
    #     suggestions.append(p.exitcode)
    # print suggestions
    qli = {}
    timeinf = {}
    totalQ= 3942354
    # csv_loc = 'aql.csv'
    # df = pd.read_csv(csv_loc, sep=',', header=0) #http://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_csv.html
    # df.to_pickle("./aql.pkl")
    # df['query'] # would select a column called name
    # This would show observations which start with STARBUC
    # match = df['query'].str.contains('(^merit)')
    # print(df['query'][match].value_counts())
    # print(match)
    df = pd.read_pickle("./aql.pkl")
    ind = pd.DataFrame(columns=['token', 'id', 'count', 'time'])
    session = pd.DataFrame(columns=['sessionId', 'sessionLength'])
    # dfquery = df[df['query'].str.contains('(^merit)', na=False)]
    # print(dfquery['query'])

    # construct term index, ind, ['token', 'id', 'count', 'time']
    # and session-time index
    for index, row in df.iterrows():
        term = row['query'].split()[0]
        if ind['token'].str.contains('term').all() == 0:
            date_time_str = row['time']
            date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
            newrow = {'token': term, 'id': {row['id']}, 'count': 1, 'time': {date_time_obj}}
            ind.append(newrow, ignore_index=True)
        else:
            updaterow = ind.loc[ind['token'] == term]
            x = updaterow['count'].astype(int)
            x += 1
            updaterow['count'] = x
            updaterow['id'].append(row['id'])
            updaterow['time'].append(row['time'])
            ind.loc[ind['token'] == term] = updaterow
    # just printing to see what it looks like
    for i in range(6):
        print(ind.loc[i])



    print("--- %s seconds ---" % (time.time() - start_time))



# def main():
#     logger.info('Executing ql indexing module')
#     logger.info('Reading file')
#     u = doc_utilities()
#     u.read_data_set(file='aql.txt', docs=1)
#     #u.read_data_set(file='data/wikipedia_text_files.csv', docs=120)
#     logger.info('Task1 - Number of documents = {}'.format(u.get_number_documents()))
#
#     # Instantiate our presistent object
#     memory_unit = persist_index_memory()
#
#     # Files can be in any format, let's convert them into a
#     # json array, in this format:
#     '''
#     doc1 = {'id': 1, 'text': txt1}
#     doc2 = {'id': 2, 'text': txt2
#     doc3 = {'id': 3, 'text': txt3}
#     doc4 = {'id': 4, 'text': txt4}
#     doc5 = {'id': 5, 'text': txt5}
#     '''
#     u.process_documents_for_indexing()
#
#     # Now let's instantiate our inverted index code
#     i_i = inverted_index(memory_unit)
#
#     # Let's transform our collection as an array of
#     # JSON elements.
#     #u.process_documents_for_indexing()
#
#     # Now let's create our index
#     i_i.create_index(collection=u.get_collection_json(),
#                      preprocessing_text=False)
#     logger.info('Index size = {}'.format(i_i.get_index_size()))
#
#     r=i_i.lookup_query('man')
#     print(r)
#     logger.info('Done Indexing')
#
#
# if __name__ == "__main__":
#     main()
