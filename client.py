from pymongo import MongoClient
import pymongo
import riotwatcher as rw
from riotwatcher import RiotWatcher
from riotwatcher import LoLException
import time
import json
import platform

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

with open('settings.json') as f:
	settings = json.load(f)
	region = settings['region']
	summoner_name = settings['summonerName']
	key = settings['apikey']

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
		pass

#find which champion they are playing
champion_id = None
for player in game["participants"]:
	if player["summonerId"] == summoner_id:
		champion_id = player["championId"]

wait_for_request()

# find other matches where they played that champion
matches = watcher.get_match_history(summoner_id, region=region, chapion_ids=[champion_id])

wait_for_request()

# TO DO
# find matches on the relevant map if possible and add item builds to files.

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
# save on windows
elif platform.system() == 'Windows' or platform.system.startswith("CYGWIN_NT"):
	directory = "C:/Riot Games/League of Legends/Config/Champions/" + champion_key + "/Recommended/LolBuilder.json"
	with open(directory, 'w+') as f:
		json.dump(json_data, f)
		print "saved build"
else:
	print("no os found")