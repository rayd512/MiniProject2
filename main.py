from bsddb3 import db
import re

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
    
    Procedure:
        1- Split by space, save it in a list
        2- iterate through list, split by ":"
        3- Otherwise, split by "><" : Assign to Ray (Do Regex pls)
        4- Create a set per query, and intersect all of the sets

    subj:gas
    (subj, gas)
    if key[0] == 'subj':
        db_key = s + key[1]

    Email : should be fine, just tell me the database is em : ['em', 'to-abc@gmail.com']
    Term : should be fine, just tell me the database is te : ['te', 's-gas'], ['te', 'confidential%'] 
    
    Date : Need to tell me if it's >, <, >=, <= : ['da', '30-12-2012', '<' / '<=' / '>' / '>=' / ':']
    
    Mode Change : ['Mode Change', 'Full' / 'Brief']
    
    Ray: [{}]
    Ray: ['s-gas', date>12-12-2012]
    Ibrahim : [(12, 13, 15), (12, 13)] -> (12, 13)
    Daniel: [(12, 13), True/False] -> Either full or brief Email
    key = s-gas
'''

def getPair(line):
    pattern = "^(.*?):(.*?)$"
	
    match = re.search(pattern, line)
    if not match:
        return None

    key = match.group(1)
    rec = match.group(2)
    return (key, rec)

def main():
    #Get an instance of BerkeleyDB
    database = db.DB()
    database.open("re.idx")
    cur = database.cursor()

    # iter = cur.first()
    # while (iter):
    #     # print(cur.count()) #prints no. of rows that have the same key for the current key-value pair referred by the cursor
    #     print(iter)

    #     #iterating through duplicates
    #     dup = cur.next_dup()
    #     while(dup!=None):
    #         print(dup)
    #         dup = cur.next_dup()

    #     iter = cur.next()

    iter = cur.first()
    while iter:
        print(iter[0].decode("utf-8"), iter[1].decode("utf-8"))
        # if int(iter[0].decode("utf-8")) == 5:
            # print("Key = 5")
        iter = cur.next()

    cur.close()
    database.close()

if __name__ == "__main__":
    main()
