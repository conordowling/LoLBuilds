from pymongo import MongoClient
import pymongo
import riotwatcher as rw
from riotwatcher import RiotWatcher
from riotwatcher import LoLException
import time
import progressbar
from optparse import OptionParser
import json

CHALLENGER_DB = "challenger"
CHALLENGER_GAMES = "challenger_games"
CHALLENGER_SUMMONERS = "challenger_summoners"

URL = "98.216.209.75"

#frodo621 key
key = "45fbe47f-84f1-43b6-9394-9f433a23d522"

class MongoDBUpdateTable:
    def __init__(self, db, collection, url="127.0.0.1", port="27017"):
        self.url = url
        self.port = port
        self.db = db
        self.collection = collection
        self.connection = MongoClient("mongodb://"+url+":"+port)
        
        self.queue = self.connection[self.db][self.collection]
        
    def pop(self):
        return self.queue.find_one({},None,[("timestamp",pymongo.ASCENDING)])
        #return self.connection[self.db].command("findandmodify", self.collection, query = {}, sort = {"_id": pymongo.ASCENDING}, remove=True)
        
    def push(self, obj):
    	obj["timestamp"] = time.time()
    	self.queue.insert(obj)

    def update(self, obj):
    	existing = self.queue.find({"player":obj["player"], "region":obj["region"]})
    	if existing == None:
    		self.push(obj)
    	else:
    		self.queue.update({'_id':existing['_id']}, {"time":time.time()})

def deep_player_scrape(self):
	pass


def shallow_player_scrape(self):
	pass


summoner_table = MongoDBUpdateTable(CHALLENGER_DB, CHALLENGER_SUMMONERS, url = URL)
games_table = MongoDBUpdateTable(CHALLENGER_DB, CHALLENGER_GAMES, url=URL)

watcher = RiotWatcher(key)

def wait_for_request():
    while not watcher.can_make_request():
        time.sleep(0.1)

for region in ['br','eune','euw','kr','lan','las','na','oce','ru','tr']:
	players = map(lambda x: (x['playerOrTeamName'], x['playerOrTeamId']), watcher.get_challenger(region = region)['entries'])
	print players
	for player in players:
		summoner_table.push({"player":player[0], "region":region, "id":player[1]})
