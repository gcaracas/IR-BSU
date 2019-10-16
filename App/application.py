from flask import Flask, Response, render_template, request
import json
import sys
sys.path.insert(0, '/Users/jason.smith/Documents/GitHub/IR-BSU/Indexing')
from fart import fart
from search import search
# from Indexing.search import search
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    # form = SearchForm(request.form)
    if request.method == "POST":
        # data = {}
        query = request.form['query']
        # with open('results.json') as json_file:
        #     data = json.load(json_file)
        # forward_message = data
        data = search(query)
        # forward_message = "<hr><h1>Your search: " + query + "</h1><br>"
        # for key in data:
        #     forward_message += "<h2>Title: " + key['title'] + "</h2><br>"
        #     forward_message += "<p>" + key['snippet'] + "</p>"
        return render_template('index.html', query=query, results=data)
    return render_template("index.html")

@app.route('/search/', methods=['POST'])
def searchreq():
    data = fart.fart()
    return data
    # forward_message = data
    # return render_template('index.html', forward_message=forward_message)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
