from pymongo import MongoClient
import pymongo
import riotwatcher as rw
from riotwatcher import RiotWatcher
from riotwatcher import LoLException
import time
import json
import platform

region = "na"
summoner_name = "frodo621"

def get_item_build(champion_key):

	item_build = {
	    "title": "The name of the page",
	    "type": "custom",
	    "map": "any",
	    "mode": "any",
	    "priority": False,
	    "sortrank": 0,
	    "blocks": [
	        {
	            "type": "A block with just boots",
	            "recMath": False,
	            "minSummonerLevel": -1,
	            "maxSummonerLevel": -1,
	            "showIfSummonerSpell": "",
	            "hideIfSummonerSpell": "",
	            "items": [
	                {
	                    "id": "1001",
	                    "count": 1
	                }
	            ]
	        }
	    ]
	}
	return item_build


def wait_for_request():
    while not watcher.can_make_request():
        time.sleep(0.1)

#frodo621 key
key = "45fbe47f-84f1-43b6-9394-9f433a23d522"

watcher = RiotWatcher(key)

summoner_id = watcher.get_summoner(name=summoner_name, region = region)['id']

game_found = False
while not game_found:
	try:
		wait_for_request()
		game = watcher.get_current_game(summoner_id)
		print game
		game_found = True
	except Exception as e:
		print "failed"

champion_id = None
for player in game["participants"]:
	if player["summonerId"] == summoner_id:
		champion_id = player["championId"]

wait_for_request()

champ_data = watcher.static_get_champion(champion_id, region=region)
print "CHAMP DATA"
print champ_data
champion_key = champ_data["key"]

json_data = get_item_build(champion_key)

# save on a mac
if platform.system() == 'Darwin':
	directory = "/Applications/League of Legends.app/Contents/LoL/Config/Champions/" + champion_key + "/Recommended/LolBuilder.json"
	with open(directory, 'w+') as f:
		json.dump(json_data, f)
		print "saved build"
elif platform.system() == 'Windows':
	directory = "C:/Riot Games/League of Legends/Config/Global/" + champion_key + "/Recommended/LolBuilder.json"
	with open(directory, 'w+') as f:
		json.dump(json_data, f)
		print "saved build"
