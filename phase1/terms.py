import re
from phase1_helpers import *

def terms():

	xml = open("1k.xml", "r")

	terms_txt = open("terms.txt", "w+")

	xml_lines = xml.readlines()

	for line in xml_lines:
		match = re.search('(<mail>)(.*)(</mail>)', line)
		if match:
			# Obtain <row> number
			row = stripTag('row', match.group(2), '[0-9]+')

			# Obtain <subj> string
			subj_match = stripTag('subj', match.group(2), '.*')
			# Obtain a list of the terms
			subjTerms = getTerms(subj_match)
			# Write each term to terms.txt in the correct format
			for each in subjTerms:
				str = "s-" + each + ":" + row + "\n"
				terms_txt.write(str)

			# Obtain <body> string
			body_match = stripTag('body', match.group(2), '.*')
			# Obtain a list of terms
			bodyTerms = getTerms(body_match)
			# Write each term to terms.txt in the correct format
			for each in bodyTerms:
				str = "b-" + each + ":" + row + "\n"
				terms_txt.write(str)

	xml.close()
	terms_txt.close()

if __name__ == "__main__":
	terms()