'''generate emails ( for testing )
creates random emails.
format:
id:abcd@pqrs.com
subject:some random subject
body:email body goes here.;

Creates email using the random list of user ids and random subject topics ( semantically un-meaningful )
Writes the list of emails to file: ./data/random_emails.txt

'''

def get_random_name_list(length):
	'''returns a list of size 'length' containing
	random_names of the format: first_last'''
	import re
	import random
	# file random_names_long.txt contains more words
	f = open('./data/random_names.txt').read()		
	names = re.split('\n', f)		# size of the list is currently 1000
	random.shuffle(names)
	if(length > len(names)):
		print "length of name list required is too big"
		print 'returning only ' + str(len(names)) + ' names'
		length = len(names)
	return names[:length]

def generate_msg_body(length):
	'''Generate a random email body
	having length number of words'''
	import re
	import random
	f = open('./data/random_words.txt').read()
	words = re.split('\n', f)
	random.shuffle(words)
	if length > len(words):
		print "Length of message can't be more than"
		print len(words)
		print "Changing the size of message to " + str(len(words))
		length = len(words)
	
	msg = ""
	for i in range(length):
		msg += words[i]
		msg += " "
	return msg

def create_random_email( num ):
	from random import randint
	'''create #num emails'''
	emails = []
	names = get_random_name_list(num)
	for i in range(num):
		# generate an email of the length between 10 to 100 words
		# And subject length 2 to 5
		msg = generate_msg_body(randint(10,20))
		subject = generate_msg_body(randint(2,6))
		emails.append((names[i], subject, msg))
	return emails

def main():
	emails = create_random_email(10)
	email_file = open('./data/random_emails.txt','w')
	for i in range(len(emails)):
		email_file.write('id:'+emails[i][0]+'\n')
		email_file.write('subject:'+emails[i][1]+'\n')
		email_file.write('body:'+emails[i][2]+';')
	email_file.close()

if __name__ == "__main__":
	main()