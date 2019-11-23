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

	special_annotations = '&lt;|&gt;|&amp;|&apos;|&quot;|&#[0-9]*;'
	special_chars = '[^a-zA-Z\d/\-\_]'
	term_pattern = '([a-z\-\d\_]{3,})'

	# Remove special annotations
	parsed = re.sub(special_annotations, " ", str)
	# Remove special chars and convert to lower case
	parsed = re.sub(special_chars, " ", parsed).lower()
	# Obtain all terms within str
	return re.findall(term_pattern, parsed)

# Obtain email match contained in from, to , cc, bcc fields
#
# Input:
# tag - the html tags. Either from, to, cc, or bcc
# str - the input string containing emails surrounded by tags
#
# Output: 
# A match object
def emailMatch(tag, str):

	# matches comma separated emails
	cs_email_pattern = '([a-zA-Z0-9\._%+-]+\@[a-zA-Z0-9\.-]+\.[a-zA-Z]+(,?\s?))*'

	tag_pattern = '<' + tag + '>' + cs_email_pattern + '</' + tag + '>'

	match = re.search(tag_pattern, str)

	return match