from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.core.mail import send_mail
from .forms import ContactForm

import sys
sys.path.append('../database/')
import dbInfo

AVG_FG = 3
AVG_FT = 4

TOT_TPM = 12
TOT_REB = 13
TOT_AST = 14
TOT_STL = 15
TOT_BLK = 16
TOT_TO = 17
TOT_PTS = 18

ARSH = ('arshdeep sidhu', 0)
JOBAN = ('joban dhindsa', 1)
KARNVIR = ('karnvir basra', 2)
SARTAJ = ('sartaj sidhu', 3)
JATIN = ('jatin bains', 4)
ANGAD = ('angad ghag', 5)
JUSTIN = ('justin kooner', 6)
HARMAN = ('harman wahid', 7)
HARVIR = ('harvir dhindsa', 8)
AJAY = ('ajay sandhu', 9)



# def home(request):
# 	template = loader.get_template('teams/personal/index.html')
# 	context = {}
		
# 	return HttpResponse(template.render(context, request))

def home(request):
	
	all_teams = dbInfo.teams.find({})

	owners = []
	for team in all_teams:
		owners.append(team["_id"])

	template = loader.get_template('teams/index.html')
	context = {
		'owners':owners
	}
		
	return HttpResponse(template.render(context, request))

def send_email(request):
	if request.method == 'POST':

		form = ContactForm(request.POST)

		if form.is_valid():
			name = form.cleaned_data['name']
			message = form.cleaned_data['message']
			email = form.cleaned_data['email']

		send_mail(name, message, email, ['sidhu.a1998@gmail.com'])

	return HttpResponseRedirect('/')

def rankings(request):

	all_teams = dbInfo.teams.find({})

	stat_index = [AVG_FG,AVG_FT,TOT_TPM,TOT_REB,TOT_AST,TOT_STL,TOT_BLK,TOT_TO,TOT_PTS]
	team_index = [ARSH, JOBAN, KARNVIR, SARTAJ, JATIN, ANGAD, JUSTIN, HARMAN, HARVIR, AJAY]
	tuple_totals = [[],[],[],[],[],[],[],[],[]]
	rankings = [['Arshdeep Sidhu'],['Joban Dhindsa'],['Karnvir Basra'],['Sartaj Sidhu'],['Jatin Bains'],['Angad Ghag'],['Justin Kooner'],['Harman Wahid'],['Harvir Dhindsa'],['Ajay Sandhu']]

	for teams in all_teams:
		tmpData = [*teams.values()]

		for i in range(9):
			tmpTup = (teams["_id"], tmpData[stat_index[i]])
			tuple_totals[i].append(tmpTup)

	for tot in tuple_totals:
		tot.sort(key = lambda tup: tup[1], reverse = True)
		print(tot)

	#Sort turnovers the correct way
	tuple_totals[7].sort()

	for tot in tuple_totals:
		for i in range(10):
			if (tot[i][0] == ARSH[0]): rankings[ARSH[1]].append(i+1)
			elif (tot[i][0] == JOBAN[0]): rankings[JOBAN[1]].append(i+1)
			elif (tot[i][0] == KARNVIR[0]): rankings[KARNVIR[1]].append(i+1)
			elif (tot[i][0] == SARTAJ[0]): rankings[SARTAJ[1]].append(i+1)
			elif (tot[i][0] == JATIN[0]): rankings[JATIN[1]].append(i+1)
			elif (tot[i][0] == ANGAD[0]): rankings[ANGAD[1]].append(i+1)
			elif (tot[i][0] == JUSTIN[0]): rankings[JUSTIN[1]].append(i+1)
			elif (tot[i][0] == HARMAN[0]): rankings[HARMAN[1]].append(i+1)
			elif (tot[i][0] == HARVIR[0]): rankings[HARVIR[1]].append(i+1)
			elif (tot[i][0] == AJAY[0]): rankings[AJAY[1]].append(i+1)

	template = loader.get_template('teams/rankings.html')
	context = {
		"rankings":rankings
	}
	return HttpResponse(template.render(context, request))

def tradecompare(request):

	all_teams = dbInfo.teams.find({})

	owners = []
	for team in all_teams:
		owners.append(team["_id"])

	template = loader.get_template('teams/tradeCompare.html')
	context = {
		'owners':owners
	}
	return HttpResponse(template.render(context, request))

def loadOwners(request):

	owner = request.GET.get('owner')

	team_info = dbInfo.teams.find_one({"_id":owner})
	players_on_teams = team_info["players"]

	context = {
		'players': players_on_teams
	}

	return JsonResponse(context, safe=False)

def analyzeTrade(request):

	print(request.POST)
	
	# if request.method == 'POST':
    # form = YourForm(request.POST)


	template = loader.get_template('teams/tradeAnalysis.html')
	context = {}
	return HttpResponse(template.render(context, request))
