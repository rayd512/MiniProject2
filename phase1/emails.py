# Note in testing emails.py:
# The provided 10-emails.txt file lacks a line:
# to-western.price.survey.contacts@ren-6.cais.net:5

import re
from phase1_helpers import *

def emails():

	xml = open("1k.xml", "r")

	emails_txt = open("emails.txt", "w+")

	xml1 = xml.readlines()

	for x in xml1:
		match = re.search('(<mail>)(.*)(</mail>)', x)
		if match:
			# Obtain <row> number
			row = stripTag('row', match.group(2), '[0-9]+')

			# Obtain <from> email(s)
			from_match = emailMatch('from', match.group(2))
			if from_match:
				# Parse comma-separated emails
				emails = re.findall('[a-zA-Z0-9\._%+-]+\@[a-zA-Z0-9\.-]+\.[a-zA-Z]+', from_match.group(0))
				for email in emails:
					emails_txt.write('from-' + email + ':' + row + '\n')

			# Obtain <to> email(s)
			to_match = emailMatch('to', match.group(2))
			if to_match:
				# Parse comma-separated emails
				emails = re.findall('[a-zA-Z0-9\._%+-]+\@[a-zA-Z0-9\.-]+\.[a-zA-Z]+', to_match.group(0))
				for email in emails:
					emails_txt.write('to-' + email + ':' + row + '\n')
				
			# Obtain <cc> email
			cc_match = emailMatch('cc', match.group(2))
			if cc_match:
				# Parse comma-separated emails
				emails = re.findall('[a-zA-Z0-9\._%+-]+\@[a-zA-Z0-9\.-]+\.[a-zA-Z]+', cc_match.group(0))
				for email in emails:
					emails_txt.write('cc-' + email + ':' + row + '\n')

			# Obtain <bcc> email
			bcc_match = emailMatch('bcc', match.group(2))
			if bcc_match:
				# Parse comma-separated emails
				emails = re.findall('[a-zA-Z0-9\._%+-]+\@[a-zA-Z0-9\.-]+\.[a-zA-Z]+', bcc_match.group(0))
				for email in emails:
					emails_txt.write('bcc-' + email + ':' + row + '\n')


if __name__ == "__main__":
	emails()