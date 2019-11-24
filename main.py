from bsddb3 import db
import re

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
    pattern = "^((subj|body)\s*:)?\s*([0-9a-zA-Z_-]+%?)$"
	
    match = re.match(pattern, line)
    if not match:
        return None

    if match.group(1) == None:
        value = match.group(3)
    else:
        value = "%s-%s" % (str(match.group(1))[0], match.group(3))

    return ["te", value]

def parseDate(line):
    pattern = "^(date)\s*(<=|<|>|>=|:)\s*(\d{4}/\d{2}/\d{2})$"

    match = re.match(pattern, line)

    
    if not match:
        return None

    return ["da", match.group(2).strip(), match.group(3).strip()]

def splitInput(line):
    pass


def parseEmail(line):
    pattern = "(from|to|cc|bcc)\s*:\s*(([0-9a-zA-Z_-]+.?)*@([0-9a-zA-Z_-]+.?)*)"

    match = re.match(pattern, line)

    if not match:
        return None

    key = "%s-%s" % (match.group(1).lower(), match.group(2).lower())
    return ["em", key]



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

if __name__ == "__main__":
    print(parseDate("date=2001/03/10"))
    print(parseEmail("from:ben@yahoo.com"))
    print(parseTerm("subj:gas"))
