
def read_audio_input():
	'''This method takes user voice as
	input and returns a string as output.
	Uses Google audio API to convert audio to text
	NOTE: number of request per day is limited to 100.'''
	import speech_recognition as sr
	r = sr.Recognizer()
	m = sr.Microphone()
	try:
		print("Starting up. Please remain quiet.")
		with m as source: r.adjust_for_ambient_noise(source)
		print("Hi there! I am jarvis. What do you want me to do?")
		first_time = True
		while True:
			if not first_time:
				print "Try again please"
			first_time = False
			with m as source: audio = r.listen(source)
			print("Got it. Give me a moment please!")
			flag = 1
			try:
				# recognize speech using Google Speech Recognition
				value = r.recognize_google(audio)
				# we need some special handling here to correctly print unicode characters to standard output
				if str is bytes:  # this version of Python uses bytes for strings (Python 2)
					command_input = format(value).encode("utf-8")
					print(u"You said {}".format(value).encode("utf-8"))
				else:  # this version of Python uses unicode for strings (Python 3+)
					print("You said {}".format(value))
			except sr.UnknownValueError:
				flag = 0
				print("Oops! Didn't catch that")
			except sr.RequestError as e:
				flag = 0
				print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
			if flag == 1: 
				break
	except KeyboardInterrupt:
		pass
	return command_input

def categorize_command( input_string ):
	'''converts the input command to a more fine grained 
	command to make it easier to understand'''
	input_string = input_string.lower()
	possible_list = input_string.split()
	
	# news fetch
	if "news" in possible_list:
		ind = possible_list.index( "news" )
		if( ind + 2 < len( possible_list ) ):
			if possible_list[ind+1] == "on":
				category = possible_list[ind+2]
				return ["news", category]
		else:
			return ["news"]
	
	# terminal start commands
	elif "start" in possible_list\
	or "run" in possible_list\
	or "open" in possible_list:
		print "cmd command detected."
		ind = -1 
		try:
			ind = possible_list.index("start")
		except ValueError:
			a = 1+1 # do nothing
		try:
			ind = possible_list.index("open")
		except ValueError:
			a = 1+1 # do nothing
		try:
			ind = possible_list.index("run")
		except ValueError:
			a = 1+1 # do nothing
		return ["run", possible_list[1].lower() + ".exe"]

	# fetching emails command
	elif "email" in possible_list\
	 or "emails" in possible_list:
		return ["email"]

	# PC shutdown related commands
	elif "shutdown" in possible_list:
		if "cancel" in possible_list:
			return ["CANCEL_SHUTDOWN"] 
		elif "minutes" in possible_list:
			time_to_shut = possible_list[possible_list.index("minutes")-1]
			return ["SHUTDOWN", time_to_shut]
		elif "minute" in possible_list:
			time_to_shut = possible_list[possible_list.index("minute")-1]
			return ["SHUTDOWN", time_to_shut]
		else:
			return ["SHUTDOWN"]


def run_on_cmd( process_name ):
	import os
	os.system("start " + process_name)


def shutdown_pc( power_off_flag, time_dur=120 ):
	import os
	if( power_off_flag == "SHUTDOWN"):
		print "System will shutdown in 2 minutes"
		os.system("shutdown -s -t " + str(time_dur))
	elif ( power_off_flag == "CANCEL_SHUTDOWN"):
		os.system("shutdown -a")
		print "Scheduled shutdown was cancelled"

class news_item():
	def __init__(self):
		a = 1 + 1
		# define news item object here.

def get_news(topic):
	'''Gets the description of news from newsapi.org from some random sources'''
	from news_preprocessor import get_news_source_list as src_obj
	from api_getter import get_api_key as gak
	from random import sample
	import requests
	import json

	api_key = gak('news_org_api')
	src_list = src_obj()
	src_len = len(src_list)
	rand_src = sample( range(src_len), 3)

	news_item_json = []
	for i in rand_src:
		news_src = src_list[i]
		print 'Feteching news from '+ news_src.name
		sorter = ""
		if news_src.is_popular_poss:
			sorter = "&sortBy=popular"
		elif news_src.is_latest_poss:
			sorter = "&sortBy=latest"
		elif news_src.is_top_poss:
			sorter = "&sortBy=top"
		url = 'https://newsapi.org/v1/articles?source='+news_src.id+sorter+'&apiKey='+api_key
		print url
		responses = requests.get(url)
		sources_json = responses.json()
		news_item_json.append(sources_json)
	print news_item_json
	return news_item_json


def print_pretty(json_string):
	'''Converts json object to human readable text.'''
	#TODO: implement this function ASAP
	a = 1 + 1

def process_audio_command():
	#TODO: un-comment these lines after testing.
	input_command = read_audio_input()
	fine_command = categorize_command(input_command)
	print fine_command
	if(fine_command == None):
		print "Sorry, I didn't understand that!\nTry again."
	command_len = len( fine_command )
	if fine_command[0] == "news":
		if command_len == 2:
			# when a category is specified.
			return get_news(fine_command[1])
		else:
			# when no category is specified.
			# TODO: finish this part first.
			# then the other part.
			return get_news("")

	elif fine_command[0] == "run":
		run_on_cmd( fine_command[1])
		return None
	elif fine_command[0] == "email":
		from email_fetcher import show_emails
		print "showing emails.."
		show_emails()
	elif fine_command[0] == "SHUTDOWN" or fine_command[0] == "CANCEL_SHUTDOWN":
		print "shutdown flag:" + fine_command[0]
		if(command_len == 2 ):
			shutdown_pc(fine_command[0], int(fine_command[1])*60)
		else:
			shutdown_pc(fine_command[0],120)

process_audio_command()