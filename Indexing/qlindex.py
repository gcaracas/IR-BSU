import collections
import itertools
from threading import Thread
# import Queue
import json
import multiprocessing
import time
import os, pickle
import pandas as pd
from datetime import datetime
from dateutil.parser import parse
import csv
import pdb
from collections import Counter
import nltk
from collections import defaultdict
from nltk.stem.snowball import EnglishStemmer  # Assuming we're working with English
import shelve
import logging

from numpy import take

def score(lst, cq, cqCount, qCount, word, index, q):
    """
    Compute the score of each CQ
    """
    # totalQ = 3942354 #pre-processed
    maxQ = 83677 #pre-processed
    maxSeshLength = 7943141.0 #pre-processed
    # freq(cq): frequency of the candidate query / maximum frequency of any query
    # mod(cq,q): number of sessions in which q is modified to cq / total number of sessions q appears
    # time(cq,q): minimum diff between the time occurence of q and cq / longest session

    freqCQ = cqCount / maxQ
    modCQ = cqCount / qCount
    timeCQ = 0 / maxSeshLength
    dinominator = 1 - min(freqCQ, modCQ)
    minDiff = []
    if q:
        for cand in lst[cq]:
            for c in q:
                if cand["id"] == c["time"]:
                    minDiff.append(abs(cand[1]-c[1]))
        if len(minDiff) > 0:
            timeCQ = min(minDiff) / maxSeshLength
            dinominator = 1 - min(freqCQ, modCQ, timeCQ)

    numerator = freqCQ + modCQ + timeCQ
    return(numerator / dinominator)


# number of total queries in aql = 3942354

def look(word, index, tok1):
    """
    Lookup a word in the index
    """
    word = word.lower()
    tword = word.split()
    tokens = len(tword)
    c = {}
    for key in tok1[tword[0]]:
        curr = index.iat[key,1]
        temp = {}
        if(len(curr.split()) >= tokens):
            for val in range(0,tokens):
                if tword[val] != curr.split()[val]:
                    break
                if val == tokens-1:
                    temp = {"id": index.iat[key,0], "time": index.iat[key,2]}
                    if curr in c.keys():
                        c[curr].append(temp)
                    else:
                        c[curr] = [temp]

    qCount = len(c)
    Scores = {}
    qprime = False
    if word in c.keys():
        qprime = c[word]
    for cand in c.keys():
        if word != cand:
            Scores[cand] = score(c, cand, len(c[cand]), qCount, word, index, qprime)

    retlist = collections.OrderedDict()
    #
    for key, value in sorted(Scores.items(), key=lambda item: item[1], reverse=True):
        retlist[value] = key
    x = 8
    if len(Scores) < x:
        x = len(Scores)
    i = 0
    vals = collections.OrderedDict()
    for val in retlist.keys():
        vals[val] = retlist[val]
        i +=1
        if i == x:
            break
    return(vals)



def convertTime():
    """
    Method to convert all the date-time values in querylog into seconds
    """
    id = 0
    csv_loc = 'aql.csv'
    with open(csv_loc, "rb") as infile,open("aqlT.csv", "wb") as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        for row in reader:
            newR = row
            if(id > 0):
                t = datetime.strptime(newR[2], '%Y-%m-%d %H:%M:%S')
                newR[2] = int(time.mktime(t.timetuple()))
            writer.writerow(newR)
            print(newR)
            id+=1



def makeSesh():
    """
    Method to make session index for calculations
    :return:
    """
    csv_loc = 'aqlT.csv'
    s = dict()
    with open(csv_loc, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] in s:
                s[row[0]].append(float(row[2]))
            else:
                s[row[0]] = [float(row[2])]
            # print(sessions[row[0]])
    return s

def makeDoc():
    """
    This will convert index csv into pickle
    """
    csv_loc = 'aqlT.csv'
    ind = pd.read_csv(csv_loc)
    ind.to_pickle("./index.pkl")
    # return ind

def makeGrams():
    """
    Method to create token dictionary and save as shelve
    """
    csv_loc = 'aqlT.csv'
    ind = dict()
    i = 0
    with open(csv_loc, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[1] in ind:
                ind[row[1]].append(i)
            else:
                ind[row[1]] = [i]
            i+=1
    with shelve.open('queries') as s:
        s['queries'] = ind
    print(len(ind))
    #     sessions = s['sessions']

def makeFirsts():
    """
    Method to create token dictionary and save as shelve
    """
    csv_loc = 'aqlT.csv'
    ind = dict()
    i = 0
    with open(csv_loc, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[1].split()[0] in ind:
                ind[row[1].split()[0]].append(i)
                i += 1
            else:
                ind[row[1].split()[0]] = [i]
                i += 1
    with shelve.open('aqltokens', writeback=True) as s:
        s['aqltokens'] = ind

def makeSeconds():
    """
    Method to create bigram dictionary and save as shelve
    """
    csv_loc = 'aqlT.csv'
    ind = dict()
    i = -1
    with open(csv_loc, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            i+=1
            if len(row[1].split()) > 1:
                tok = row[1].split()[0] + " " + row[1].split()[1]
                if tok in ind:
                    ind[tok].append(i)
                    # i += 1
                else:
                    ind[tok] = [i]
                    # i += 1
    with shelve.open('secs') as s:
        s['secs'] = ind

def makeThirds():
    """
    Method to create trigram dictionary and save as shelve
    """
    csv_loc = 'aqlT.csv'
    ind = dict()
    i = -1
    with open(csv_loc, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            i+=1
            if len(row[1].split()) > 2:
                tok = row[1].split()[0] + " " + row[1].split()[1] + " " + row[1].split()[1]
                if tok in ind:
                    ind[tok].append(i)
                    # i += 1
                else:
                    ind[tok] = [i]
                    # i += 1
    with shelve.open('secs') as s:
        s['secs'] = ind

# def main():
# def sugg(q):
def sugg(q, tok1):
    logging.basicConfig(filename='logging.log', level=logging.DEBUG)
    # with shelve.open('tokens') as s:
    #     freq = s['tokens']
    # with shelve.open('firsts') as s:
    #     tok1 = s['firsts']
    # with shelve.open('secs') as s:
    #     tok2 = s['secs']
    index = pd.read_pickle("index.pkl")
    start_time = time.time()
    # q = "to"
    # suggestions = []

    # totalQ= 3942354
    # maxSeshLength = 7943141.0
    # sessions = makeSesh()
    # csv_loc = 'aqlT.csv'
    # # i = 0
    # with open(csv_loc, "r") as file:
    #     reader = csv.reader(file)
    #     for row in reader:
    #         index.add(row)


    # makeGrams()
    # makeFirsts()
    # makeSeconds()
    # with shelve.open('queries') as s:
    #     freq = s['queries']
    # max = 0
    # for key in freq.keys():
    #     if len(freq[key]) > max:
    #         max = len(freq[key])

    # print(max)
    # index = pd.read_pickle("index.pkl")

    # index = pickle.load(infile)
    # print(index.head(n=5))
    # with shelve.open('index') as s:
    #     # s['index'] = index
    #     index = s['index']



    # with shelve.open('sesh') as s:
    #     # s['sessions'] = sessions
    #     sessions = s['sessions']
    # # print(sessions)
    # print(index.lookup("first"))
    # # sugglist = index.lookup(q)
    # m = []
    # for x in sessions:
    #     m.append(max(sessions[x]) - min(sessions[x]))
    #
    # print(max(m))

    return look(q, index, tok1)

    # sugglist = look(q, index, tok1)
    # retval = []
    # for x in sugglist:
    #     retval.append(x[1])
    #     y = x.__getitem__(1)
    # return(retval)
    # return(dict.fromkeys(retval,0))


    # print(index.lookup('first'))
    # for id in index.query(word):
    #     print(id)

    # getWC()

    # a = shelve.open("freq.db", writeback=True)
    # data = a['counts']
    # print(data['stones'] + data['childs'])
    # a.close()

    # df = pd.read_csv(csv_loc, sep=',', header=0) #http://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_csv.html
    # df.to_pickle("./aql.pkl")
    # df['query'] # would select a column called name
    # This would show observations which start with STARBUC
    # match = df['query'].str.contains('(^merit)')
    # print(df['query'][match].value_counts())
    # print(match)
    # df = pd.read_pickle("./aql.pkl")
    # ind = pd.DataFrame(columns=['token', 'id', 'count', 'time'])
    # ind = dict.fromkeys('token', 'id', 'count', 'time')
    # ind = {}
    # session = pd.DataFrame(columns=['sessionId', 'sessionLength'])
    # # dfquery = df[df['query'].str.contains('(^merit)', na=False)]
    # # print(dfquery['query'])
    # with open(csv_loc, mode='r') as infile:
    #     reader = csv.reader(infile)
    #     with open(csv_loc)
    # # construct term index, ind, ['token', 'id', 'count', 'time']
    # # and session-time index
    # i = 0
    # for index, row in df.iterrows():
    #     term = row['query'].split()[0]
    #     if ind['token'].str.contains('term').all() == 0:
    #         date_time_str = row['time']
    #         date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
    #         newrow = {'token': term, 'id': {row['id']}, 'count': 1, 'time': {date_time_obj}}
    #         ind.append(newrow, ignore_index=True)
    #     else:
    #         updaterow = ind.loc[ind['token'] == term]
    #         x = updaterow['count'].astype(int)
    #         x += 1
    #         updaterow['count'] = x
    #         updaterow['id'].append(row['id'])
    #         updaterow['time'].append(row['time'])
    #         ind.loc[ind['token'] == term] = updaterow
    # # just printing to see what it looks like
    # for i in range(6):
    #     print(ind.loc[i])

    # indn1= {}
    # sessionind = {}


    # convertTime()
    print("--- %s seconds ---" % (time.time() - start_time))

def main():
    makeFirsts()
if __name__ == "__main__":
    main()
