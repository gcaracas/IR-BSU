import pickle
import logging
from classes.utilities import doc_utilities
from classes.persist_index_memory import persist_index_memory
from classes.inverted_index import inverted_index
from tqdm import tqdm
import pandas as pd
import matplotlib.pyplot as plt
import sys
max_unique_words_index = 500000

def main():
    docs=[]
    eiv=[]
    u = doc_utilities()
    u.read_data_set(file='data/wikipedia_text_files.csv')
    #u.process_documents_for_indexing()
    
    elems=5000000
    sampling=10000
    count_sampling=0
    val_prev=0
    with tqdm(total=elems, desc="Indexing documents", bar_format="{l_bar}{bar} [ time left: {remaining} ]") as pbar:
        for i in range(elems):
            if count_sampling == sampling:
                docs = u.collection.head(i).text.str.split().tolist()
                val_prev = len(list(set([ d for txt in docs for d in txt])))
                count_sampling = 0
            else:
                count_sampling=count_sampling+1
            eiv.append(val_prev)  
            docs.append(i)
            pbar.update(1)
    print('done')
    plt.figure(figsize=(6, 4), dpi=70)
    plt.loglog(docs, eiv, marker=".")
    plt.title("Docs/Unique tokens")
    plt.xlabel("Documents")
    plt.ylabel("Unique words")
    plt.grid(True)
    plt.savefig('heap.png')





    sys.exit()

    docs=[]
    vocab=[]
    eiv=[]
    print('processing')
    #vocab = [len(list(set(doc['text'].split())))  for doc in collection[:100000]]
    #with tqdm(total=len(u.get_collection_json()), desc="Indexing documents", bar_format="{l_bar}{bar} [ time left: {remaining} ]") as pbar:
    #    for doc in u.get_collection_json():
    #        i_i.index_documen(document=doc,
    #                           preprocessing=False)
    #        pbar.update(1)
    elems=1000000
    sampling=10000
    count_sampling=0
    val_prev=0
    with tqdm(total=elems, desc="Indexing documents", bar_format="{l_bar}{bar} [ time left: {remaining} ]") as pbar:
        for i,doc in enumerate(collection[:elems]):
            vocab=vocab+doc['text'].split()
            docs.append(i)
            if count_sampling==sampling:
                val_prev=len(set(vocab))
                count_sampling=0
            else:
                count_sampling=count_sampling+1
            eiv.append(val_prev)  
            '''
            dd=list(set([str(d) for d in doc['text'].split()]))
            for dd1 in dd:
                vocab.append(dd1)
            vocab=list(set(vocab))
            eiv.append(len(vocab))
            docs.append(i)
            '''
            pbar.update(1)
    print('done')
    plt.figure(figsize=(6, 4), dpi=70)
    plt.loglog(docs, eiv, marker=".")
    plt.title("Docs/Unique tokens")
    plt.xlabel("Documents")
    plt.ylabel("Unique words")
    plt.grid(True)
    plt.savefig('heap.png')

main()
