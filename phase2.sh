sort phase1/10-recs.txt --unique | perl break.pl | db_load -T -t hash re.idx
sort phase1/10-terms.txt --unique | perl break.pl | db_load -T -t btree te.idx
sort phase1/10-emails.txt --unique | perl break.pl | db_load -T -t btree em.idx
sort phase1/10-dates.txt --unique | perl break.pl | db_load -T -t btree da.idx