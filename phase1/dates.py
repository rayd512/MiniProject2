import re
from phase1_helpers import *

def dates(file):

	xml = open(file, "r")

	dates_txt = open("dates.txt", "w+")

	xml_lines = xml.readlines()

	for line in xml_lines:
		match = match = re.search('(<mail>)(.*)(</mail>)', line)
		if match:
			row = stripTag('row', match.group(2), '[0-9]+')
			date_match = stripTag('date', match.group(2), '.*')
			dates_txt.write(date_match + ':' + row + '\n')

	xml.close()
	dates_txt.close()
	return

if __name__ == "__main__":
	dates()