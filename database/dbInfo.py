import pymongo, sys
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://arshDB:arshDBpass@cluster0-hbjvs.mongodb.net/test?retryWrites=true&w=majority")
db = cluster["FantasyBasketball"]
players = db["Players"]
teams = db["Teams"]