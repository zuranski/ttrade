import urllib2,smtplib
from bs4 import BeautifulSoup
from email.mime.text import MIMEText

def getWebData(category,query):

	web_data=[]
	
	ttradeFile=urllib2.urlopen('http://ttrade.tigerapps.org/?items=100&category='+category+'&listingType=A&order=N&query='+(query if query else ''))
	ttradeHTML=ttradeFile.read()

	soup=BeautifulSoup(ttradeHTML)
	listings=soup.find('div',{'id':'listings'}).find_all('div',{'class':'listing'})
	for listing in listings:

		try: index=int(listing['id'])
		except ValueError: continue

		try: price=float(listing.find('span',{'class':'tr tc_t'}).decode_contents())
		except ValueError:  price=0.

		title=listing.find('span',{'class':'tr tc_title'}).decode_contents()
		web_data.append({'id':index,'title':title,'price':price})

	return web_data

def sendmail(address,subject,message):	

	s=smtplib.SMTP('localhost')
	msg=MIMEText(message)
	msg['Subject']=subject
	msg['From']='zuranski@localhost'
	msg['To']=address
	s.sendmail(msg['From'],[msg['To']],msg.as_string())
	s.close()
