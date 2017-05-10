# This function gets the api key for the api link : web_word
def get_api_key( web_word ):
	import re
	api_key_list = open('./data/API_KEY.txt','r').read()
	word_list = re.split(':|\n', api_key_list)
	ind = word_list.index(web_word)
	api_key = word_list[ind+1]
	return api_key

