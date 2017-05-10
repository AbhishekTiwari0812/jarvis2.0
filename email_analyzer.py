def get_feedback_model():
	import re
	feedback_model = {}
	f = open('./data/email_feedback.txt').read();	
	feedback_data = re.split('\n', f)
	for i in feedback_data:
		if len( i ) == 0:
			continue
		word_data = re.split(' ', i)
		feedback_model[word_data[0]] = (int(word_data[1]), int(word_data[2]))
	return feedback_model

def score_list( words, model ):
	'''Takes input a list of words,
	returns the score'''
	score = 0
	for i in words:
		if i in model:
			score += model[i][1]
		else:
			score += 2.5
	# normalized score
	score = score / len(words)
	return score

def stem_words( l ):
	suffix_list = [ 'ed', 'd', 'ing', 'ly', 's', 'es', 'ous',\
	'acity', 'al', 'ance', 'ion','hood', 'able', 'ible', 'ish',\
	'ism','ity', 'ive', 'less', 'like', 'ness', 'ship','wise'];
	ans = []
	for i in l:
		flag = False
		string_len = len( i )
		for j in [4,3,2,1]:
			if string_len >= j:
				suffix = i[string_len - j :]
				if suffix in suffix_list:
					ans.append( i[:string_len-j] )
					flag = True
					break
		if flag is False:
			ans.append(i)
	#TODO: Add method for removing the prefixes as well.
	return ans

def remove_stop_words( l ):
	f = open('./data/stop_word.txt')
	word_list = f.read().lower().split()	
	word_list = stem_words(word_list)
	new_list = []
	for i in range( len( l ) ):
		if l[i] not in word_list and len( l[i] ) > 1 :
			new_list.append( l[i] )
	return new_list

def preprocess_email( email ):
	'''takes input a string,
	returns a list of important words'''
	import re
	words = email.lower()
	word_list = re.split(';|,|\\!|\\.| |\\?|"|-|&|\n|\'', email)
	word_list = stem_words( word_list )
	word_list = remove_stop_words( word_list )
	return word_list

def email_value( email ):
	'''takes input a tuple, (from, subject, body)
	and returns the value of the email'''
	print "Computing the ratings of email from " + email[0]
	import re
	FROM_CONTRIBUTION = 0.3
	SUBJECT_CONTRIBUTION = 0.2
	BODY_CONTRIBUTION = 0.5
	model = get_feedback_model()
	final_score = 0
	temp_list = ["id_holder"]
	temp_list[0] = email[0]
	final_score = FROM_CONTRIBUTION * score_list(temp_list, model)
	final_score += SUBJECT_CONTRIBUTION * score_list( preprocess_email(email[1]), model)
	final_score += BODY_CONTRIBUTION * score_list( preprocess_email(email[2]), model)
	print "score: " + str(final_score)
	return final_score

def rate_and_sort(email_list):
	'''Takes input a list of email tuples and
	returns a sorted list of tuples in the order 
	of the most preferred to lease preferred'''
	print "Analyzing the unread emails."
	size = len(email_list)
	emails_with_val = []
	for i in range(size):
		if len(email_list[i]) < 3:
			print "There's a problem in email:"+str(email_list[i])
			print "Skipping analysis"
			continue
		print "printing email:"
		print email_list[i]
		emails_with_val.append( ( email_value(email_list[i][:]),\
		email_list[i][0], email_list[i][1], email_list[i][2] ) )
	
	emails_with_val = sorted(emails_with_val, key=lambda x: x[0])
	size = len(emails_with_val)
	sorted_emails = []
	for i in range(len(emails_with_val)):
		sorted_emails.append([ emails_with_val[size-i-1][1],\
			emails_with_val[size-i-1][2],\
			emails_with_val[size-i-1][3] ])
	return sorted_emails
