import datetime
from sys import argv
import os

def new(entry):
	if entry == '':
		return
	with open('/home/tsx525/.journal/.journal', 'a') as f:
		f.write("%s - %s\n" % (
			str(datetime.datetime.today().strftime('%Y-%m-%d %X')), entry))

def listEntrys():
	search = raw_input('>>>')
	os.system('cat /home/tsx525/.journal/.journal | grep %s' % search)

def loop():
	while True:
		entry = raw_input(datetime.datetime.today().strftime('%Y-%m-%d %X - '))
		if entry == ':q':
			break
		if entry == ':s':
			listEntrys()
			continue
		new(entry)

loop()