from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import sys

sys.path.append('../database/')

#hacky fix so I don't need connection string in file
import dbInfo 

# Create your views here.
def index(request):
	
	all_teams = dbInfo.teams.find({})

	owners = []
	for team in all_teams:
		owners.append(team["_id"])

	template = loader.get_template('teams/index.html')
	context = {
		'owners':owners
	}
		
	return HttpResponse(template.render(context, request))

def detail(request, team_id):

	team_info = dbInfo.teams.find_one({"_id":team_id})
	teamData = [*team_info.values()]
	
	players_on_teams = team_info["players"]
	contextData = []

	for p in players_on_teams:
		player = dbInfo.players.find_one({"_id":p.lower().rstrip()})
		if(player != None):
			contextData.append([*player.values()]) #* unpacks dict values
		else:
			contextData.append([p,"N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A"])


	template = loader.get_template('teams/generic.html')
	context = {
		'teamData':teamData[2:18],
		'data':contextData,
		'players':players_on_teams
	}

	return HttpResponse(template.render(context, request))



