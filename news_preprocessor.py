# news preprocessing script
# must be run at least once 
# to get the news through JARVIS 2.0

def get_source_online():
	'''Creates the list of sources available
	with their categories. Writes the details to data/news_source.txt file'''
	import requests
	import json
	import io
	print 'getting the details of all news sources...'
	responses = requests.get('https://newsapi.org/v1/sources?language=en')
	sources_json = responses.json()
	news_sources = './data/news_sources_json.txt'
	import io, json
	with io.open(news_sources, 'w', encoding='utf-8') as f:
		f.write(json.dumps(sources_json, ensure_ascii=False))
	print 'wrote the details successfully to news_source_json.txt file'


class news_source():
	def __init__(self, source_details):
		self.id = source_details['id']
		self.name = source_details['name']
		self.description = source_details['description']
		self.url = source_details['url']
		self.category = source_details['category']
		self.language = source_details['language']
		self.country = source_details['country']
		temp = source_details['sortBysAvailable']
		self.is_top_poss = 'top' in temp
		self.is_latest_poss = 'latest' in temp
		self.is_popular_poss = 'popular' in temp


def get_news_source_list():
	'''Parses the news resources file to get the details of news channels.'''
	import json 
	try:
		f = open('./data/news_sources_json.txt','r')
	except IOError:
		print 'Couldn\'t find news sources file. Trying to download'
		get_source_online()
		try:
			f = open('./data/news_sources_json.txt','r')
		except IOError:
			print 'Couldn\'t download news sources.'
	data = f.read()
	parsed_json = json.loads(data)
	news_source_list = [ ]
	for element in parsed_json['sources']:
		dict_form = json.loads( json.dumps( element, ensure_ascii=False).encode('utf8') )
		news_source_obj = news_source(dict_form)
		news_source_list.append(news_source_obj)
	return news_source_list

