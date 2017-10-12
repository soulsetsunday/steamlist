from django.db import models
import requests, bs4
#for Steam age gate:
cookies = { 'birthtime': '283993201', 'mature_content': '1' }
#User-agent, because why not
headers = { 'user-agent': 'Tiny scraping thing demo'}

class Game:
	def __init__(self, game_name, app_id, logo_hash, playtime_forever):
		self.name = game_name
		self.appid = app_id
		self.logo = 'http://media.steampowered.com/steamcommunity/public/images/apps/{}/{}.jpg'.format(app_id, logo_hash)
		self.hours_played = playtime_forever
		#self.review_score = scrapeReviews(app_id)
		self.review_score = 0
	def __repr__(self):
		return self.name

def scrapeReviews (appid):
	store_url = 'http://store.steampowered.com/app/{}'.format(appid)
	res = requests.get(store_url, cookies = cookies, headers = headers)
	store = bs4.BeautifulSoup(res.content, "html.parser")
	review = store.select('#review_histogram_rollup_section div:nth-of-type(1) div span:nth-of-type(1)')
	#some (old? delisted?) games have no review score
	#steam needs at least 10(?) reviews for a score
	#the expected format is '##, some things return 'cc
	if len(review) > 0: 
		try:
			score = int(review[0].get('data-store-tooltip')[:2])
		except ValueError:
			score = 0
		return score
	return 0
