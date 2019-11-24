from bsddb3 import db
import re
termPattern = "^((subj|body)\s*:)?\s*([0-9a-zA-Z_-]+%?)$"
datePattern = "^(date)\s*(<=|<|>|>=|:)\s*(\d{4}/\d{2}/\d{2})$"
emailPattern = "(from|to|cc|bcc)\s*:\s*(([0-9a-zA-Z_-]+.?)*@([0-9a-zA-Z_-]+.?)*)"
outputPattern = "((?:output=full)|(?:output=brief))"
queryPattern = "^((?:(?:(?:subj|body)\s*:)?\s*(?:[0-9a-zA-Z_-]+%?))|(?:(?:date)\s*(?:<=|<|>|>=|:)\s*(?:\d{4}/\d{2}/\d{2}))|(?:(?:from|to|cc|bcc)\s*:\s*(?:(?:[0-9a-zA-Z_-]+.?)*@(?:[0-9a-zA-Z_-]+.?)*)))((?:\s{1}(?:(?:(?:(?:subj|body)\s*:)?\s*(?:[0-9a-zA-Z_-]+%?))|(?:(?:date)\s*(?:<=|<|>|>=|:)\s*(?:\d{4}/\d{2}/\d{2}))|(?:(?:from|to|cc|bcc)\s*:\s*(?:(?:[0-9a-zA-Z_-]+.?)*@(?:[0-9a-zA-Z_-]+.?)*))))*)$"
'''
	Available Databases:
		1-Re.idx (Records): 
			Type: Hash
			Key: Row ID
			Value: Entire email
		2-te.idx (Terms):
			Type: Btree
			Key: Term (Subject/Body)
			Value: Row ID
		3-em.idx (Emails):
			Type: Btree
			Key: Email (from, to, cc, bcc)
			Value: Row ID
		4-da.idx (Dates):
			Type: Btree
			Key: Date (of the email)
			Value: Row ID
	
	Procedure:
		1- Split by space, save it in a list
		2- iterate through list, split by ":"
		3- Otherwise, split by "><" : Assign to Ray (Do Regex pls)
		4- Create a set per query, and intersect all of the sets

	subj:gas
	(subj, gas)
	if key[0] == 'subj':
		db_key = s + key[1]

	key = s-gas
'''

def parseTerm(line):
	
	
	match = re.match(termPattern, line)
	if not match:
		return None

	if match.group(1) == None:
		value = match.group(3)
	else:
		value = "%s-%s" % (str(match.group(1))[0], match.group(3))

	return ["te", value]

def parseDate(line):
	

	match = re.match(datePattern, line)

	
	if not match:
		return None

	return ["da", match.group(2).strip(), match.group(3).strip()]

def splitInput(line):
	match = re.match(queryPattern, line)
	if not match:
		match = re.match(outputPattern, line)
		if not match:
			return None
		else:
			return str(match.group(1))

	queries = []

	queries.append(str(match.group(1)))

	lines = re.split(queryPattern, line)

	fixArray(lines)

	recursiveSplit(lines[-1], queries)

	# print(queries)
	return queries


def recursiveSplit(line, queries):
	match = re.match(queryPattern, line)
	if not match:
		return

	lines = re.split(queryPattern, line)

	fixArray(lines)
	queries.append(lines[0])
	if len(lines) == 1:
		return
	recursiveSplit(lines[-1], queries)


def fixArray(lines):
	while("" in lines): 
		lines.remove("")

	for i, s in enumerate(lines):
		lines[i] = s.strip()



def parseEmail(line):
	

	match = re.match(emailPattern, line)

	if not match:
		return None

	key = "%s-%s" % (match.group(1).lower(), match.group(2).lower())
	return ["em", key]

def processQuery(line):
	queries = splitInput(line)
	parsed = []

	if len(queries) == 1 and (queries[0] == "brief" or queries[0] == "full"):
		return queries[0]

	for i in queries:
		temp = parseEmail(i)
		if temp:
			parsed.append(temp)
		temp = parseDate(i)
		if temp:
			parsed.append(temp)
		temp = parseTerm(i)
		if temp:
			parsed.append(temp)

	print(parsed)

def main():
	#Get an instance of BerkeleyDB
	database = db.DB()
	database.open("em.idx")
	
	cur = database.cursor()
	iter = cur.first()
	while iter:
		print(iter[0].decode("utf-8"), iter[1].decode("utf-8"))
		iter = cur.next()
	cur.close()
	database.close()
	# pass
if __name__ == "__main__":
	print(parseDate("date<=2001/03/10"))
	print(parseEmail("from:ben@yahoo.com"))
	print(parseTerm("subj:gas"))
	processQuery("body:stock confidential shares date<2001/04/12")
# (((from|to|cc|bcc)\s*:\s*(([0-9a-zA-Z_-]+.?)*@([0-9a-zA-Z_-]+.?)*))|((date)\s*(<=|<|>|>=|:)\s*(\d{4}/\d{2}/\d{2}))|(((subj|body)\s*:)?\s*([0-9a-zA-Z_-]+%?)))+
# ((((subj|body)\s*:)?\s*([0-9a-zA-Z_-]+%?))|((date)\s*(<=|<|>|>=|:)\s*(\d{4}/\d{2}/\d{2}))|((from|to|cc|bcc)\s*:\s*(([0-9a-zA-Z_-]+.?)*@([0-9a-zA-Z_-]+.?)*)))+