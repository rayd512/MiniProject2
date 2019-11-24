import re
from phase1_helpers import *

def recs(file):

	xml = open(file, "r")

	recs_txt = open("recs.txt", "w+")

	xml_lines = xml.readlines()

	for line in xml_lines:
		match = re.search('(<mail>)(.*)(</mail>)', line)
		if match:
			row = stripTag('row', match.group(2), '[0-9]+')
			recs_txt.write(row + ':' + match.group(0) + '\n')

	xml.close()
	recs_txt.close()
	return


if __name__ == "__main__":
	recs()