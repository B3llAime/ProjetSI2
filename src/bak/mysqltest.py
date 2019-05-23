import MySQLdb

db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="root", # your username
                      passwd="a", # your password
                      db="test_db") # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor() 

# Use all the SQL you like
if cur.execute("select * from test_db.testtable where name='"+'arun'+"'"):
	print 'success';
else:
	print 'fail';

# print all the first cell of all the rows
for row in cur.fetchall() :
    print row[0],row[1]
