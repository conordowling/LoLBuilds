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

class MongoDBSafe:
    def __init__(self, db, collection, url="127.0.0.1", port="27017"):
        self.url = url
        self.port = port
        self.db = db
        self.collection = collection
        self.connection = MongoClient("mongodb://"+url+":"+port)
        
    def push(self, doc):
        return self.connection[self.db][self.collection].insert(doc)
    
    def get(self, doc):
        return self.connection[self.db][self.collection].find_one(doc)
    
def deep_player_scrape():
	pass


def shallow_player_scrape(summoner_id, region):
	retrieved = False
	while not retrieved:
		try:
			wait_for_request()
			match_history = watcher.get_match_history( summoner_id, region=region )
			retrieved = True
			print("got match history")
		except Exception as e:
			print e

	match_ids = map(lambda x: x["matchId"], match_history["matches"])
	for match_id in match_ids:
		if not games_table.get({"matchId":match_id, "region":region}):
			retrieved = False
			while not retrieved:
				try:
					wait_for_request()
					match = watcher.get_match(match_id, region=region, include_timeline=True)
					games_table.push(match)
					retrieved = True
				except Exception as e:
					pass

	return



summoner_table = MongoDBUpdateTable(CHALLENGER_DB, CHALLENGER_SUMMONERS, url = URL)
games_table = MongoDBSafe(CHALLENGER_DB, CHALLENGER_GAMES, url=URL)

watcher = RiotWatcher(key)

def wait_for_request():
    while not watcher.can_make_request():
        time.sleep(0.1)

for region in ['NA','EUW','KR','EUNE','LAN','LAS','BR','OCE','RU','TR']:
	wait_for_request()
	players = map(lambda x: (x['playerOrTeamName'], x['playerOrTeamId']), watcher.get_challenger(region = region.lower())['entries'])
	print players
	for player in players:
		print(player)
		summoner_table.push({"player":player[0], "region":region, "id":player[1]})
		shallow_player_scrape(player[1], region.lower())
