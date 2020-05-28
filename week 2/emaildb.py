import sqlite3
conn=sqlite3.connect('emaildb.sqlite')
cur=conn.cursor()     # Used to work across the database

cur.execute('DROP TABLE IF EXISTS Counts')    #If there is already a table counts then it will be deleted
cur.execute('CREATE TABLE Counts(org TEXT,count INTEGER)')

fname=input('Enter file name: ')
fh=open(fname)
for line in fh:
    if not line.startswith('From '): continue
    word=line.split()
    email=word[1]
    parts=email.split('@')
    org=parts[1]
    cur.execute('SELECT count FROM Counts WHERE org = ?',(org,) )
    row=cur.fetchone()
    if row is None:                             #If there is no row of that organisation
        cur.execute('''INSERT INTO Counts(org,count)
                        VALUES(?,1)''',(org,))
    else:                                      #If row already exists then it is updated
        cur.execute('''UPDATE Counts
                        SET count=count+1
                        WHERE org=?''',(org,))
conn.commit()

#creating database to display output
sqlstr='SELECT org,count FROM Counts ORDER BY count DESC LIMIT 10'
for row in cur.execute(sqlstr):
    print(str(row[0]),row[1])
cur.close()
