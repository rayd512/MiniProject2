from bsddb3 import db
from connection import Connection
import re
from phase1.phase1_helpers import *

termPattern = "^((subj|body)\s*:)?\s*([0-9a-zA-Z_-]+%?)$"
datePattern = "^(date)\s*(<=|<|>|>=|:)\s*(\d{4}/\d{2}/\d{2})$"
emailPattern = "(from|to|cc|bcc)\s*:\s*(([0-9a-zA-Z_-]+.?)*@([0-9a-zA-Z_-]+.?)*)"
outputPattern = "(?:output=(full))|(?:output=(brief))"
queryPattern = "^((?:(?:(?:subj|body)\s*:)?\s*(?:[0-9a-zA-Z_-]+%?))|(?:(?:date)\s*(?:<=|<|>|>=|:)\s*(?:\d{4}/\d{2}/\d{2}))|(?:(?:from|to|cc|bcc)\s*:\s*(?:(?:[0-9a-zA-Z_-]+\.?)*@(?:[0-9a-zA-Z_-]+\.?)*)))((?:\s{1}(?:(?:(?:(?:subj|body)\s*:)?\s*(?:[0-9a-zA-Z_-]+%?))|(?:(?:date)\s*(?:<=|<|>|>=|:)\s*(?:\d{4}/\d{2}/\d{2}))|(?:(?:from|to|cc|bcc)\s*:\s*(?:(?:[0-9a-zA-Z_-]+.?)*@(?:[0-9a-zA-Z_-]+.?)*))))*)$"

'''
Displays the row id and value of a query in either full or brief format
Input:
    keys - an array(ordered) or set(unordered) of strings referencing the key 
           of the value to be displayed.
    isFull - a boolean to determine display option (full or brief).
             True for full, brief otherwise.
Output:
    None
'''
def display(keys, isFull):
    database = db.DB()
    database.open("re.idx")
    cursor = database.cursor()

    for each in keys:
        # Keys in byte format and utf-8 encoded
        key = bytes(str(each), 'utf-8')
        # Result contains key and value pair
        result = cursor.set(key)
        rowID = result[0].decode('utf-8')
        unparsed_value = result[1].decode('utf-8')

        match = re.search('(<mail>)(.*)(</mail>)', unparsed_value)
        subj = stripTag('subj', match.group(2), '.*')

        # Brief format
        if(not(isFull)):
            # Obtain <subject> string
            print(rowID + ', subj: ' + subj)
        # Full format (id, date, emails, subj, body)
        else:
            date = stripTag('date', match.group(2), '.*')
            body = stripTag('body', match.group(2), '.*')
            # Replace special annotations
            annotations = ['&lt;', '&gt;', '&amp;', '&apos;', '&quot;', '&#10;']
            symbol = ["<", ">", "&", "'", "\"", "\n"]
            for i in range(0, len(annotations)):
            	body = re.sub(annotations[i], symbol[i], body)

            print('ID: ' + rowID)
            print('date: ' + date)
            printEmails(match.group(2))
            print('subj: ' + subj)
            print('body: ')
            print(body)
            print('===================================')

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
		value = "%s-%s" % (str(match.group(1))[0].strip(), match.group(3).strip())

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
	key = "%s-%s" % (match.group(1).lower().strip(), match.group(2).lower().strip())
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

	return parsed

def main():
    #Get an Connection class
    conn = Connection()

    # Mode
    isFull = False

    while True:
        command = input("Enter command\n> ")

        if command == 'quit':
            print("Good bye")
            return

        #Change output to full/brief
        if command == 'output=full':
            isFull = True
            continue
        elif command == 'output=brief':
            isFull = False
            continue
        
        #Parse the query first
        args = processQuery(command)
        if args:
            #Then query the data and display it
            rowIDs = conn.queryData(args)
            rowIDsList = list(rowIDs)
            rowIDsList.sort()
            display(rowIDsList, isFull)
    
if __name__ == "__main__":
	main()