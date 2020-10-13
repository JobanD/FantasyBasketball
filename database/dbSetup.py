import pymongo, sys
from pymongo import MongoClient
import dbInfo #hacky fix so I don't need connection string in file

def updatePlayerDB():
	dbInfo.players.delete_many({}) #Assure DB is empty before updating

	playerPosts = []
	for playerData in open("../data/TestData1.csv", encoding="ISO-8859-1"):
		#foreach player in file
		playerInfo = playerData.split(",")

		if playerInfo[0] == "PLAYER":
			continue

		playerPost = {
			"_id":playerInfo[0].lower(),
			"rank":playerInfo[1],
			"fg":playerInfo[3],
			"ft":playerInfo[4],
			"threePt":playerInfo[5],
			"tReb":playerInfo[6],
			"assists":playerInfo[7],
			"steals":playerInfo[8],
			"blocks":playerInfo[9],
			"turnovers":playerInfo[10],
			"pts":playerInfo[11],
			"fgZ":playerInfo[16],
			"ftZ":playerInfo[17],
			"threePtZ":playerInfo[18],
			"tRebZ":playerInfo[19],
			"assistsZ":playerInfo[20],
			"stealsZ":playerInfo[21],
			"blocksZ":playerInfo[22],
			"turnoversZ":playerInfo[23],
			"ptsZ":playerInfo[24]
		}

		playerPosts.append(playerPost)

	try:
		dbInfo.players.insert_many(playerPosts)
	except pymongo.errors.BulkWriteError as bwe: #try/catch for any duplicates
		print(bwe.details)
		raise

def updateTeamsDB():
	dbInfo.teams.delete_many({}) #Assure Teams are empty

	teamPosts = []
	for teamData in open("../data/TeamData1.csv", encoding="ISO-8859-1"):

		teamInfo = teamData.split(",")

		totRank = round(calcTotal("rank",teamInfo[1:14]),2)
		totFG = round(calcTotal("fg",teamInfo[1:14]),2)
		totFT = round(calcTotal("ft",teamInfo[1:14]),2)
		totTPM = round(calcTotal("threePt",teamInfo[1:14]),2)
		totReb = round(calcTotal("tReb",teamInfo[1:14]),2)
		totAst = round(calcTotal("assists",teamInfo[1:14]),2)
		totStl = round(calcTotal("steals",teamInfo[1:14]),2)
		totBlk = round(calcTotal("blocks",teamInfo[1:14]),2)
		totTO = round(calcTotal("turnovers",teamInfo[1:14]),2)
		totPts = round(calcTotal("pts",teamInfo[1:14]),2)

		avgRank = round(totRank/13,2)
		avgFG = round(totFG/13,2)
		avgFT = round(totFT/13,2)
		avgTPM = round(totTPM/13,2)
		avgReb = round(totReb/13,2)
		avgAst = round(totAst/13,2)
		avgStl = round(totStl/13,2)
		avgBlk = round(totBlk/13,2)
		avgTO = round(totTO/13,2)
		avgPts = round(totPts/13,2)

		teamPost = {
			"_id":teamInfo[0].lower(),
			"players":teamInfo[1:14],

			"avgRank":avgRank,
			"avgFG":avgFG,
			"avgFT":avgFT,
			"avgTPM":avgTPM,
			"avgReb":avgReb,
			"avgAst":avgAst,
			"avgStl":avgStl,
			"avgBlk":avgBlk,
			"avgTO":avgTO,
			"avgPts":avgPts,

			"totTPM":totTPM,
			"totReb":totReb,
			"totAst":totAst,
			"totStl":totStl,
			"totBlk":totBlk,
			"totTO":totTO,
			"totPts":totPts
		}

		teamPosts.append(teamPost)

	try:
		dbInfo.teams.insert_many(teamPosts)
	except pymongo.errors.BulkWriteError as bwe: #try/catch for any duplicates
		print(bwe.details)
		raise

def calcTotal(cat, team):
	tot = 0.0
	for player in team:
		# print(player)
		pInfo = dbInfo.players.find_one({"_id":player.lower().rstrip()})
		if(pInfo):
			tot += float(pInfo[cat])
		# print(players.find_one({"id":player.lower()}))
		#Costly look into $sum
	return tot

if len(sys.argv) < 2:	
	print("Enter proper arguments (1, 2 or 3)")
else:
	if sys.argv[1] == "1":
		updatePlayerDB()
		print("Loaded Players")
	elif sys.argv[1] == "2":
		updateTeamsDB()
		print("Loaded Teams")
	elif sys.argv[1] == "3":
		updatePlayerDB()
		updateTeamsDB()
		print("Loaded Players and Teams")
	#used for testing
	elif sys.argv[1] == "4": 
	#test code goes here
		for teamData in open("../data/TeamData1.csv", encoding="ISO-8859-1"):
			teamInfo = teamData.split(",")
			print(teamInfo[1:14])

	else:
		print("Enter proper arguments (1,2 or 3)")
