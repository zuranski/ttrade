import sys,argparse,MySQLdb as mdb
from db_actions import *
from web_actions import *

parser=argparse.ArgumentParser()
parser.add_argument('category', type=str, help='options Ho (housing) Au (Autos) Bi (Bicycles)')
parser.add_argument('--query', type=str, help='query string')
parser.add_argument('--email', type=str, help='email')
args=parser.parse_args()

### connect
try:
	db=mdb.connect(host='localhost',user='zuranski',db='ttrade')
except mdb.Error, e:
	if args.email:
		sendmail(args.email,'Restart database',"Error %d: %s" % (e.args[0],e.args[1]))
	sys.exit(1)

### get data from db
if not checkTableExists(db,args.category): createTable(db,args.category)
db_data=getTable(db,args.category)
db_ids=set([int(row['id']) for row in db_data])
		
### get listings from website
web_data=getWebData(args.category,args.query)
web_ids=set([int(row['id']) for row in web_data])

### remove old data
indicesToRemove=db_ids.difference(web_ids)
removeFromTable(db,args.category,indicesToRemove)

### add new entries and email
indicesToAdd=web_ids.difference(db_ids)
if len(indicesToAdd)>0:
	dataToAdd=[row for row in web_data if row['id'] in indicesToAdd]
	addToTable(db,args.category,dataToAdd)

	### send an email
	if args.email:
		subject='New entries in category %s for query %s. Check tigertrade'%(args.category,args.query)
		message="\n".join( str(item['title']+' --- '+str(item['price'])+\
		'$ link: http://ttrade.tigerapps.org/item/'+str(item['id'])) for item in dataToAdd)
		sendmail(args.email,subject,message)
	
db.commit()
db.close()
sys.exit(0)
