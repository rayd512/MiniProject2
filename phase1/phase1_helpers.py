import re


# Strips opening and closing html tags
#
# Input:
# tag - the html tag to be stripped
# str - the string to be parsed
# 
# Output:
# The input string w/o the tag
def stripTag(tag, str, pattern):

	ptrn = '(<' + tag + '>)(' + pattern + ')(</' + tag + '>)'
	match = re.search(ptrn, str)
	return match.group(2)


# Obtain terms contained within input string
#
# Input:
# str - the input string containing terms
#
# Output: 
# A list of terms
def getTerms(str):

	# Remove special annotations
	parsed = re.sub('&lt;|&gt;|&amp;|&apos;|&quot;|&#[0-9]*;', " ", str)
	# Remove special chars and convert to lower case
	parsed = re.sub('[^a-zA-Z\d/\-\_]', " ", parsed).lower()
	# Obtain all terms within str
	return re.findall('([a-z\-\d\_]{3,})', parsed)


# Obtain email match contained in from, to , cc, bcc fields
#
# Input:
# tag - the html tags. Either from, to, cc, or bcc
# str - the input string containing emails surrounded by tags
#
# Output: 
# A match object containing emails
def emailMatch(tag, str):

	# Obtain comma separated emails as one match
	cs_email_pattern = '([a-zA-Z0-9\._%+-]+\@[a-zA-Z0-9\.-]+\.[a-zA-Z]+(,?\s?))*'

	tag_pattern = '<' + tag + '>' + cs_email_pattern + '</' + tag + '>'

	match = re.search(tag_pattern, str)

	return match

def printEmails(match):

	fields = ['from', 'to', 'cc', 'bcc']

	for field in fields:
		cs_emails = emailMatch(field, match)
		# Parse comma-separated emails
		emails = re.findall('[a-zA-Z0-9\._%+-]+\@[a-zA-Z0-9\.-]+\.[a-zA-Z]+', cs_emails.group(0))
		if (len(emails) == 1):
			print(field + ': ' + emails[0])
		elif(len(emails) > 1):
			print(field + ': ' + emails[0], end="")
			for i in range(len(emails)-1):
				print(', ' + emails[i+1], end="")
			print()
		else:
			print(field + ': ')

	return