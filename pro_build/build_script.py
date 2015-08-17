from bson.code import Code
from pymongo import MongoClient
import pymongo
import json
import time

start_time = time.time()

URL = "98.216.209.75"

db  = MongoClient("mongodb://"+URL+":27017")

map_js = Code(open('build_map.js', 'r').read())
reduce_js = Code(open('build_reduce.js','r').read())

results = db['challenger']['challenger_games'].map_reduce(map_js, reduce_js, 'pro_builds')
print time.time() - start_time, "seconds"
print results.find()