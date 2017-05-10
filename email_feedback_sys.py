import email_analyzer
def update_feedback_model(new_model):
	#print "updating the feedback model.."
	f = open('./data/email_feedback.txt','w')
	
	for i in new_model.keys():
		#print "this is I: " + i + " and :" + str( new_model[i] )
		f.write( i + ' ' + str(new_model[i][0]) +' ' + str(new_model[i][1]) + '\n')
	f.close()

def update_helper(string,rating):
	import re 
	current_model = email_analyzer.get_feedback_model()
	words = string.lower()
	word_list = re.split(';|,|\\!|\\.| |\\?|"|-|&|\n|\'', string)
	word_list = email_analyzer.stem_words( word_list )
	word_list = email_analyzer.remove_stop_words( word_list )
	new_model = current_model
	for i in word_list:
		if i in current_model:
			word_freq = 1 + current_model[i][0]
			word_rating = ( current_model[i][0] * current_model[i][1] + rating ) / word_freq
			new_model[i] = (word_freq, word_rating)
		else:
			new_model[i] = ( 1,rating )
	#print "Updated model."
	return new_model

def email_feedback( email, rating):
	'''gets an email and the rating of the email[0,5]
	and based on the rating, updates the preference table.'''
	print "Rating email...."
	print "From:" + email[0]
	for i in range(3):
		new_model = update_helper(email[i],rating)
		update_feedback_model(new_model)
	print "Finished feedback update with the email."


