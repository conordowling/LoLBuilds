from pymongo import MongoClient
import pymongo
import riotwatcher as rw
from riotwatcher import RiotWatcher
from riotwatcher import LoLException
import time
from optparse import OptionParser
import json

#frodo621 key
key = "45fbe47f-84f1-43b6-9394-9f433a23d522"

watcher = RiotWatcher(key)

print watcher.static_get_versions(region = 'na')