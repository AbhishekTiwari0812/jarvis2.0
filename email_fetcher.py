def fetch_emails():
	import re
	import email_analyzer
	print 'Fetching the unread emails.'
	f = open('./data/unread_email_test.txt').read()
	raw_email = re.split(';',f)
	email_list = []
	for i in raw_email:
		temp_email = re.split(':|\n', i)
		if( len(temp_email) != 6 ):
			print "there's format problem with email: " + str(temp_email)
			print "Skipping email."
			continue
		temp_val = [temp_email[1], temp_email[3], temp_email[5]]
		email_list.append(temp_val)
	print "Completed fetching emails."
	return email_analyzer.rate_and_sort(email_list)

def show_emails():
	import email_feedback_sys
	emails = fetch_emails()
	print "------------------\nUNREAD EMAILS::::::\n"
	for i in emails:
		print "\n\n\n-------------------------------"
		print "From: " + i[0]
		print "Subject: " + i[1]
		print "Body: " + i[2]
		print "-------------------------------"
		while True:
			rating = raw_input("Please rate this email...\nfrom 1(least favorite) to 5(most favorite):")
			rating = int(rating)
			if rating <= 5 and rating >= 1:
				break
			else:
				print "Rating must be between 1 to 5."

		email_feedback_sys.email_feedback(i, rating)

#show_emails()