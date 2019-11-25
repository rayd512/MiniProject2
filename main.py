from bsddb3 import db
import re
termPattern = "^((subj|body)\s*:)?\s*([0-9a-zA-Z_-]+%?)$"
datePattern = "^(date)\s*(<=|<|>|>=|:)\s*(\d{4}/\d{2}/\d{2})$"
emailPattern = "(from|to|cc|bcc)\s*:\s*(([0-9a-zA-Z_-]+.?)*@([0-9a-zA-Z_-]+.?)*)"
outputPattern = "(?:output=(full))|(?:output=(brief))"
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

# Checks if query is a termQuery and parses it
# Inputs: line - a potential termQuery
# Outputs: None if no match, an array if matched
def parseTerm(line):
	# Check for a match with the query(line)
	match = re.match(termPattern, line)
	if not match:
		return None

	# Check if there was a term prefix
	if match.group(1) == None:
		value = match.group(3)
	else:
		value = "%s-%s" % (str(match.group(1))[0], match.group(3))

	# Return the parsed value
	return ["te", value]


# Checks if query is a DateQuery and parses it
# Inputs: line - a potential DateQuery
# Outputs: None if no match, an array if matched
def parseDate(line):
	# Check for a match with the query(line)
	match = re.match(datePattern, line)
	# Return None is there wasn't a match
	if not match:
		return None

	# Return "da", the comparator and the date
	return ["da", match.group(2).strip(), match.group(3).strip()]

# Splits each query and returns an array of them
# Inputs: line - the input from STDIN
# Outputs: an array of query or simply just brief or full
def splitInput(line):
	# Check if input is a query or an output
	match = re.match(queryPattern, line)
	if not match:
		match = re.match(outputPattern, line)
		if not match:
			# An invalid input
			return None
		if match.group(1) != None:
			return str(match.group(1))
		else:
			return str(match.group(2))

	# Instantiate a blank array
	queries = []

	# Append the first query
	queries.append(str(match.group(1)))

	# Split the input
	lines = re.split(queryPattern, line)

	# Fix the array
	fixArray(lines)

	# Check if we need to keep splitting
	if len(lines) != 1:
		recursiveSplit(lines[-1], queries)

	# print(queries)
	return queries

# Recursively splits the input until it can't be split anymore
def recursiveSplit(line, queries):
	# Check for match
	match = re.match(queryPattern, line)
	if not match:
		return

	# Split the groups
	lines = re.split(queryPattern, line)

	# Fix the resulting array
	fixArray(lines)
	queries.append(lines[0])
	# Base case, cannot be split anymore
	if len(lines) == 1:
		return
	# Recursive call to split
	recursiveSplit(lines[-1], queries)

# Removes empty strings and whitespace in a string array
def fixArray(lines):
	# Removes all empty string in an array
	while("" in lines): 
		lines.remove("")

	# Strips any leading or trailing whitespace in each string
	for i, s in enumerate(lines):
		lines[i] = s.strip()


# Checks if query is an emailQuery and parses it
# Inputs: line - a potential email query
# Outputs: None if no match, an array if matched
def parseEmail(line):
	# Check for a match with the query(line)
	match = re.match(emailPattern, line)

	# Return none if there is no match
	if not match:
		return None

	# Build the string for email lookup
	key = "%s-%s" % (match.group(1).lower(), match.group(2).lower())
	# Return an array
	return ["em", key]

# Given a query, this functions parses it and returns values 
# that will help perform the actions the query is asking
# Inputs: line - the query from STDIN
# Outputs: queries - will either be an array of array or a string
# containing which output was chosen or None if query was invalid
def processQuery(line):
	# Split up each query
	queries = splitInput(line)
	# Create an empty list
	parsed = []
	if queries == None:
		print("Invalid query")
		return None
	# Check if the query was a mode change
	if queries == "brief" or queries == "full":
		# Return the mode 
		return queries

	# Loop through all the queries
	for i in queries:
		# Test the query on each type,
		# store the return if there was a match
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
	# print(parseDate("date<=2001/03/10"))
	# print(parseEmail("from:ben@yahoo.com"))
	# print(parseTerm("subj:gas"))
	# processQuery("body:stock confidential shares date<2001/04/12")
	# processQuery("output=brief")
	# processQuery("subj:gas")
	tests = [
	"subj:gas",
	"subj:gas body:earning",
	"confidential%",
	"from:phillip.allen@enron.com",
	"to:phillip.allen@enron.com",
	"to:kenneth.shulklapper@enron.com  to:keith.holst@enron.com",
	"date:2001/03/15",
	"date>2001/03/10",
	"bcc:derryl.cleaveland@enron.com  cc:jennifer.medcalf@enron.com",
	"body:stock confidential shares date<2001/04/12"]
	# print(tests)
	for i in tests:
		print(i)
		processQuery(i)

# (((from|to|cc|bcc)\s*:\s*(([0-9a-zA-Z_-]+.?)*@([0-9a-zA-Z_-]+.?)*))|((date)\s*(<=|<|>|>=|:)\s*(\d{4}/\d{2}/\d{2}))|(((subj|body)\s*:)?\s*([0-9a-zA-Z_-]+%?)))+
# ((((subj|body)\s*:)?\s*([0-9a-zA-Z_-]+%?))|((date)\s*(<=|<|>|>=|:)\s*(\d{4}/\d{2}/\d{2}))|((from|to|cc|bcc)\s*:\s*(([0-9a-zA-Z_-]+.?)*@([0-9a-zA-Z_-]+.?)*)))+