# news preprocessing script
# must be run at least once 
# to get the news through JARVIS 2.0

def get_sources():
	'''Creates the list of sources available
	with their categories. Writes the details to data/news_source.txt file'''
	api_keys = open('./data/API_KEY.txt','r').read()
	import re
	word_list = re.split(':|\n', api_keys)
	ind = word_list.index('news_org_api')
	news_org_api = api_keys[ind+1]
	import requests
	responses = requests.get('https://newsapi.org/v1/sources?language=en')
	sources_json = str( responses.json() )
	news_sources = open('./data/news_sources_json.txt', 'w')
	news_sources.write( sources_json )

get_sources() 

