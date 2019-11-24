import sys
from terms import terms
from emails import emails
from dates import dates
from recs import recs

def prepareDataFiles():

	if(len(sys.argv) != 2):
		if(len(sys.argv) > 2):
			print('Incorrect usage; too many arguments. Aborting')
			return
		print('Source file not found. Aborting.')	
		return

	terms(sys.argv[1])
	emails(sys.argv[1])
	dates(sys.argv[1])
	recs(sys.argv[1])

	return

if __name__ == '__main__':
	prepareDataFiles()
