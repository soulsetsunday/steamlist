from django.shortcuts import render
import requests
from django.http import HttpResponseRedirect
from .forms import SteamForm
from django.urls import reverse
import json
from .models import Game, scrapeReviews

keyFile = open('SteamApiKey.txt', 'r')
STEAMAPIKEY = keyFile.readline()[:-1]
keyFile.close()

def index(request):
	if request.method == 'POST':
		form = SteamForm(request.POST)
		if form.is_valid():
			steam_id = form.cleaned_data['form_steam_id']
			return HttpResponseRedirect(reverse('steamlist:results', args=(steam_id,)))
	else:
		form = SteamForm()
	return render(request, 'steamlist/index.html', {'form': form})

def results(request, sent_steam_id):
	#use id and key to form url, send url, recieve json
	STEAMURL = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={0}&steamid={1}&include_appinfo=1&format=json'
	res = requests.get(STEAMURL.format(STEAMAPIKEY, sent_steam_id))
	recieved_json = res.text
	try:
		parsed_json = json.loads(recieved_json)
		##
		gamelist = list()
		for x in parsed_json['response']['games']:
			if x['playtime_forever'] == 0:
				gamelist.append(Game(x['name'], x['appid'], x['img_logo_url'], x['playtime_forever']))
		##
		for x in gamelist:
			x.review_score = scrapeReviews(x.appid)
		#this sorts by review score high to low
		gamelist.sort(key=lambda x: x.review_score, reverse=True)

		return render(request, 'steamlist/results.html', {'gamelist': gamelist})
	except:
		form = SteamForm()
		return render(request, 'steamlist/index.html', {'error_message': "Something went wrong. Confirm the ID is correct, and maybe if Steam is up.", 'form': form})

	

	
