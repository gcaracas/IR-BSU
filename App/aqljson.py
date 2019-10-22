#!/usr/bin/env python
# coding: utf8
import csv
import Queue
import json
import multiprocessing
import time

def toCsv():
    with open('aql.txt', 'r') as in_file:
        stripped = (line.strip() for line in in_file)
        lines = (line.split("\t") for line in stripped if line)
        with open('aql.csv', 'w') as out_file:
            writer = csv.writer(out_file)
            writer.writerow(('id', 'query', 'time'))
            writer.writerows(lines)
# import pandas as pd
# df = pd.read_fwf('aql.txt')
# df.to_csv('aql.csv')


# aql1 = []
# with open("AQL/Clean-Data-01.txt") as f:
#     for line in f:
#         line = line.strip().split("\t")
#         if (line[0] != "AnonID"):
#             aql1.append({"id": line[0], "query": line[1], "time": line[2]})
# with open('AQL/aql1.json', 'w') as json_file:
#     json.dump(aql1, json_file)
# aql2 = []
# with open("AQL/Clean-Data-02.txt") as f:
#     for line in f:
#         line = line.strip().split("\t")
#         if (line[0] != "AnonID"):
#             aql2.append({"id": line[0], "query": line[1], "time": line[2]})
# with open('AQL/aql2.json', 'w') as json_file:
#     json.dump(aql2, json_file)
# aql3 = []
# with open("AQL/Clean-Data-03.txt") as f:
#     for line in f:
#         line = line.strip().split("\t")
#         if (line[0] != "AnonID"):
#             aql3.append({"id": line[0], "query": line[1], "time": line[2]})
# with open('AQL/aql3.json', 'w') as json_file:
#     json.dump(aql3, json_file)
# aql4 = []
# with open("AQL/Clean-Data-04.txt") as f:
#     for line in f:
#         line = line.strip().split("\t")
#         if (line[0] != "AnonID"):
#             aql4.append({"id": line[0], "query": line[1], "time": line[2]})
# with open('AQL/aql4.json', 'w') as json_file:
#     json.dump(aql4, json_file)
# aql5 = []
# with open("AQL/Clean-Data-05.txt") as f:
#     for line in f:
#         line = line.strip().split("\t")
#         if (line[0] != "AnonID"):
#             aql5.append({"id": line[0], "query": line[1], "time": line[2]})
# with open('AQL/aql5.json', 'w') as json_file:
#     json.dump(aql5, json_file)
