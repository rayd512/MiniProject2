from bsddb3 import db
import re
from phase1.phase1_helpers import *

'''
    Available Databases:
        1-re.idx (Records): 
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
    
    Ray: ['s-gas', date>12-12-2012]
    Ibrahim : [(12, 13, 15), (12, 13)] -> (12, 13)
    Daniel: [(12, 13), True/False] -> Either full or brief Email
'''

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
        key = bytes(each, 'utf-8')
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
            body = re.sub('&lt;', "<", body)
            body = re.sub('&gt;', ">", body)
            body = re.sub('&amp;', "&", body)
            body = re.sub('&apos;', "'", body)
            body = re.sub('&quot;', "\"", body)
            body = re.sub('&#10;', "\n", body)

            print('ID: ' + rowID)
            print('date: ' + date)
            printEmails(match.group(2))
            print('subj: ' + subj)
            print('body: ')
            print(body)
            print('===================================')

def main():
    # Get an instance of BerkeleyDB
    database = db.DB()
    database.open("re.idx")
    cur = database.cursor()

    # Using this set will produce same but unordered o/p
    # myStringSet = {'5', '11', '12', '13', '19', '23', '26', '27', '33', '34'}
    myStringSet = ['5', '11', '12', '13', '19', '23', '26', '27', '33', '34']
    display(myStringSet, True)

    cur.close()
    database.close()

if __name__ == "__main__":
    main()
