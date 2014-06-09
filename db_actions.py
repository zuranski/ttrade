import MySQLdb as mdb

def checkTableExists(db,tablename):
	cursor=db.cursor(mdb.cursors.DictCursor)
	cursor.execute('select * from information_schema.tables where table_name = "%s";' %tablename)
	return cursor.fetchone()!=None

def getTable(db,tablename):
	cursor=db.cursor(mdb.cursors.DictCursor)
	cursor.execute('select * from %s;' %tablename)
	return cursor.fetchall()

def createTable(db,tablename):
	cursor=db.cursor(mdb.cursors.DictCursor)
	cursor.execute('create table if not exists %s (id INT, title VARCHAR(100), \
    price FLOAT, ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP(), PRIMARY KEY (id));'%tablename)

def removeFromTable(db,tablename,indices):
	cursor=db.cursor(mdb.cursors.DictCursor)
	for index in indices:
		cursor.execute('delete from %s where id=%s;' %(tablename,index))

def addToTable(db,tablename,rows):	
	cursor=db.cursor(mdb.cursors.DictCursor)
	for row in rows:
		cursor.execute('insert into %s (id,title,price) values(%i,"%s",%f);' %(tablename,row['id'],row['title'],row['price']))
