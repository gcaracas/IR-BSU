from flask import Flask, Response, render_template, request
import json
import logging
import sys
import shelve
import pandas as pd
import pickle
import qlindex
sys.path.append("../Indexing")
from search import search
sys.path.append("../Indexing/classes")
from load_index import load_index_in_memory
# sys.path.insert(0, '/Users/jason.smith/Documents/GitHub/IR-BSU/App')
import nltk


app = Flask(__name__)

# with shelve.open('firsts') as s:
#     tok1 = s['firsts']
s={}
index={}
@app.route('/', methods=['GET', 'POST'])
def index():
    # form = SearchForm(request.form)
    if request.method == "POST":
        # data = {}
        query = request.form['query']
        # with open('results.json') as json_file:
        #     data = json.load(json_file)
        # forward_message = data
        data = search(query, index)
        print(data)
        # data = search(query)
        # forward_message = "<hr><h1>Your search: " + query + "</h1><br>"
        # for key in data:
        #     forward_message += "<h2>Title: " + key['title'] + "</h2><br>"
        #     forward_message += "<p>" + key['snippet'] + "</p>"
        return render_template('index.html', query=query, results=data)
    return render_template("index.html")

@app.route('/search/', methods=['GET'])
def suggest():
    logging.basicConfig(filename='example.log', level=logging.DEBUG)
    if request.method == "GET":
        q = request.args.get('param')
        logging.info(q)
        logging.info('q')
        logging.info(q)
        # data = qlindex.sugg(q)
        data = qlindex.sugg(q, tok1)
        # print(data)
        return data
    # forward_message = data
    # return render_template('index.html', forward_message=forward_message)

if __name__ == '__main__':
    # app.run(host="0.0.0.0", port=80)
    with shelve.open('firsts') as s:
        tok1 = s['firsts']
    nltk.download('punkt')
    i = load_index_in_memory()
    index, mem = i.load_index()
    index.storage = mem

    # for x in list(s.keys()):
    #     print(s)
    # tok1 = s['firsts']
    app.run(debug = True)
    # app.run(host="18.218.1.8", port=80)
