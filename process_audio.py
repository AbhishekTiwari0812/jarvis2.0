
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
	possible_list = input_string.split()
	
	# news fetch
	if "news" in possible_list:
		ind = possible_list.index( "news" )
		if( ind + 2 < len( possible_list ) ):
			if possible_list[ind+1] == "on":
				category = possible_list[ind+2]
				return ("news", category)
		else:
			return ("news")
	
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
		return ("run", possible_list[1].lower() + ".exe")


	elif True:
		return "no match"


def run_on_cmd( process_name ):
	import os
	os.system("start " + process_name)

def process_audio_command():
	input_command = read_audio_input()
	fine_command = categorize_command(input_command)
	command_len = len( fine_command )
	if fine_command[0] == "news":
		if command_len == 2:
			print "do nothing"
		else:
			print "do nothing anyway"
	if fine_command[0] == "run":
		run_on_cmd( fine_command[1])


process_audio_command()	