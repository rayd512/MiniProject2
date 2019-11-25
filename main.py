from bsddb3 import db
from connection import Connection
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

def main():
    #Get an Connection class
    conn = Connection()

    # Mode
    isFull = True
    
    # Temporary args
    args = [['da', '>=', '2000/10/02'], ['te','s-special'], ['em', 'to-western.price.survey.contacts@ren-6.cais.net']]

    while True:
        command = input("Enter command\n> ")
        # print(command)

        if command == 'quit':
            print("Good bye")
            return
        
        #parse command and get args
        #args = parseCommand(command)
        
        if args[0] == 'Mode Change':
            isFull = True if args[1] == 'Full' else False
            continue
        
        rowIDs = conn.queryData(args)
        print(rowIDs)

if __name__ == "__main__":
    main()
