import re

def terms():

	mail_pattern = '(<mail>)(.*)(</mail>)'

	row_pattern = '(<row>)([0-9]+)(</row>)'

	subject_pattern = '(<subj>)(.*)(</subj>)'

	body_pattern = '(<body>)(.*)(</body>)'

	term_pattern = '([a-z\-\d\_]{3,})'

	special_annotations = '&lt;|&gt;|&amp;|&apos;|&quot;|&#[0-9]*;'

	xml = open("1k.xml", "r")

	terms_txt = open("terms.txt", "w+")

	xml1 = xml.readlines()

	for x in xml1:
		match = re.search(mail_pattern, x)
		if match:
			# Obtain <row> number
			row_match = re.search(row_pattern, match.group(2))
			row = row_match.group(2)

			# Obtain <subj> string
			subj_match = re.search(subject_pattern, match.group(2))
			# Remove special annotations
			subj = re.sub(special_annotations, " ", subj_match.group(2))
			# Remove special chars and convert to lower case
			subj = re.sub(r"[^a-zA-Z\d/\-\_]", " ", subj).lower()
			# Obtain all terms within the subject
			subjTerms = re.findall(term_pattern, subj)
			# Write each term to terms.txt in the correct format
			for each in subjTerms:
				str = "s-" + each + ":" + row + "\n"
				terms_txt.write(str)

			# Obtain <body> string
			body_match = re.search(body_pattern, match.group(2))
			# Remove special annotations
			body = re.sub(special_annotations, " ", body_match.group(2))
			# Remove punctuations and convert to lower case
			body = re.sub(r"[^a-zA-Z\d/\-\_]", " ", body).lower()
			# Obtain all terms within the body
			bodyTerms = re.findall(term_pattern, body)
			# Write each term to terms.txt in the correct format
			for each in bodyTerms:
				#b-dave: 5
				str = "b-" + each + ":" + row + "\n"
				terms_txt.write(str)

	xml.close()
	terms_txt.close()

if __name__ == "__main__":
	terms()