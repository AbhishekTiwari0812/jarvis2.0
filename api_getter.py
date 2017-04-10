def get_api_key( key ):
	import re
	api_key_list = open('./data/API_KEY.txt','r').read()
	word_list = re.split(':|\n', api_key_list)
	ind = word_list.index(key)
	api_key = word_list[ind+1]
	return api_key

