import json
import urllib2
import requests

from datetime import datetime
import os

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

from apscheduler.schedulers.blocking import BlockingScheduler

def sendEMail():
	fromaddr = "InsertFromAddressHere"
	toaddr = "InsertToAddressHere"
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = "Electroneum VIP - New Block Found!!!"

	body = "Found a New Block!"
	msg.attach(MIMEText(body, 'plain'))
	 
	server = smtplib.SMTP('InsertSMTPAddressHere', 587)
	server.starttls()
	server.login(fromaddr, "InsertPasswordHere")
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()

def checkBlocks():
	response = requests.get("http://18.217.58.195:8117/stats")
	data = response.json()
	pool = data['pool']
	stats = pool['stats']
	lastBlock = int(stats['lastBlockFound'])
	
	fname = 'lastBlock.dat'
	if not os.path.exists(fname):
		with open(fname, 'w') as f:
			f.write('%d' % 0)

	with open(fname) as f:
		last = int(f.read())

	if not last == lastBlock:
		print 'New Block!'
		with open(fname, 'w') as f:
			f.write('%d' % lastBlock)
		sendEMail()

if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(checkBlocks, 'interval', seconds=60)

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass