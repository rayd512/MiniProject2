from bsddb3 import db

class Connection:
    def __init__(self):
        #Establish connections per database

        self.term_conn = db.DB()
        self.email_conn = db.DB()
        self.date_conn = db.DB()
        self.rec_conn = db.DB()

        self.term_conn.open('te.idx')
        self.email_conn.open('em.idx')
        self.date_conn.open('da.idx')
        self.rec_conn.open('re.idx')

        self.term_cursor = self.term_conn.cursor()
        self.email_cursor = self.email_conn.cursor()
        self.date_cursor = self.date_conn.cursor()
        self.rec_cursor = self.rec_conn.cursor()
    
    def getEmail(self, email):
        #Initialize an empty set, and set the cursor to the email
        rowIDs = set()
        iter = self.email_cursor.set_range(email.encode("utf-8"))
        
        if not iter or not(iter[0].decode("utf-8") == email):
            return set()
        
        rowIDs.add(int(iter[1].decode("utf-8")))

        #iterating through duplicates
        dup = self.email_cursor.next_dup()
        while(dup != None):
            rowIDs.add(int(dup[1].decode("utf-8")))
            dup = self.email_cursor.next_dup()
        
        return rowIDs


    def getTerm(self, term):
        #If term doesn't start with s- or b-, then search for both of them
        if not (term[0:2] == 's-' or term[0:2] == 'b-'):
            set1 = self.getTerm("s-"+term)
            set2 = self.getTerm("b-"+term)
            
            set1 = set1.union(set2)
            return set1

        #Otherwise, create an empty set
        rowIDs = set()

        #If term ends with %, delete the % sign, and loop through all keys that start with
        #the given term
        if term[-1] == '%':
            term_real = term.replace('%', '')
            iter = self.term_cursor.set_range(term_real.encode("utf-8"))
            if not iter or not iter[0].decode('utf-8').startswith(term_real):
                return set()
            
            while(iter and iter[0].decode('utf-8').startswith(term_real)):
                rowIDs.add(int(iter[1].decode("utf-8")))
                iter = self.term_cursor.next()
        else:
            #Otherwise, find all keys that are the given term
            iter = self.term_cursor.set_range(term.encode("utf-8"))
        
            if not iter or not(iter[0].decode("utf-8") == term):
                return set()
            
            rowIDs.add(int(iter[1].decode("utf-8")))

            #iterating through duplicates
            dup = self.term_cursor.next_dup()
            while dup:
                rowIDs.add(int(dup[1].decode("utf-8")))
                dup = self.term_cursor.next_dup()

        return rowIDs

    def getDate(self, comparator, date):
        rowIDs = set()

        #If looking for all dates greater than the given date
        if comparator == '>' or comparator == '>=':
            #Set cursor to the date
            iter = self.date_cursor.set_range(date.encode("utf-8"))
            if not iter:
                return set()

            #If we're only looking for dates greater than the given date, then skip 1
            if comparator == '>' and iter[0].decode("utf-8") <= date:
                iter = self.date_cursor.next_nodup()
            
            #Find all the Row IDs now
            while(iter):
                rowIDs.add(int(iter[1].decode("utf-8")))
                iter = self.date_cursor.next()

        #Iterate from the beginning as long as the date is smaller than the given date
        elif comparator == '<':
            iter = self.date_cursor.first()
            if not iter:
                return set()
            
            while iter and iter[0].decode('utf-8') < date:
                rowIDs.add(int(iter[1].decode("utf-8")))
                iter = self.date_cursor.next()
        #Iterate from the beginning as long as the date is smaller than or equal to the given date
        elif comparator == '<=':
            iter = self.date_cursor.first()
            if not iter:
                return set()

            while iter and iter[0].decode('utf-8') <= date:
                rowIDs.add(int(iter[1].decode("utf-8")))
                iter = self.date_cursor.next()
        else:
            #Find all the duplicate keys that have the given date
            iter = self.date_cursor.set_range(date.encode("utf-8"))
        
            if not iter or not(iter[0].decode("utf-8") == date):
                return set()
            
            rowIDs.add(int(iter[1].decode("utf-8")))

            #iterating through duplicates
            dup = self.date_cursor.next_dup()
            while(dup != None):
                rowIDs.add(int(dup[1].decode("utf-8")))
                dup = self.date_cursor.next_dup()


        return rowIDs

    def queryData(self, args):
        result = []
        #Iterate through arguments, and append the result sets
        for query in args:
            query[1] = query[1].strip()
            db_name = query[0]

            rowIDs = set()
            if db_name == 'em':
                result.append(self.getEmail(query[1]))
            elif db_name == 'te':
                result.append(self.getTerm(query[1]))
            elif db_name == 'da':
                result.append(self.getDate(query[1], query[2]))
        
        #Merge all the result sets together into 1 set
        resultSet = result[0]
        for rowIDs in result:
            resultSet = resultSet.intersection(rowIDs) 
        return resultSet
