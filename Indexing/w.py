import os, os.path
import whoosh
from whoosh import index
from whoosh.fields import Schema
import logging
from whoosh.fields import SchemaClass, ID, KEYWORD, STORED, TEXT
import pickle
import logging
from classes.utilities import doc_utilities
from tqdm import tqdm
import pandas as pd
from whoosh.writing import AsyncWriter
class MySchema(SchemaClass):
    #id = ID(stored=True, unique=True) 
    id = TEXT 
    title = TEXT
    text = TEXT
def main():
    logging.basicConfig(level=logging.DEBUG, format='%(filename)s %(levelname)s: %(asctime)s: %(message)s')
    logger = logging.getLogger('main')
    logger.info('Executing indexing module')
    logger.info('Reading file')
    du = doc_utilities()
    du.read_data_set(file='data/wikipedia_text_files.csv')
    logger.info('Task1 - Number of documents = {}'.format(du.get_number_documents()))
    du.process_documents_for_indexing()
    collection=du.get_collection_json()[0:1000000]
    
    if not os.path.exists("indexdir"):
        os.mkdir("indexdir")
    ix = index.create_in("indexdir", MySchema)
    #writer = ix.writer()
    writer = AsyncWriter(ix)
    with tqdm(total=len(collection), desc="Indexing documents", bar_format="{l_bar}{bar} [ time left: {remaining} ]") as pbar:
        for d in collection:
            text=str(d['text'])
            idt=str(d['id'])
            title=str(d['title'])
            writer.add_document(id=idt, 
                title=title,
                text=text)
            pbar.update(1)
    writer.commit()

if __name__ == "__main__":
    main()
