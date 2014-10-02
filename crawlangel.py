import StringIO
import json
import socket
import urllib
import datetime
import re
import time
import random
import socks  # SockiPy module
import stem.process
import os
from stem.util import term
from datetime import date


exits = ["us","ca"]

ipstack = [] #stacks used to track the ip and time it was last banned
timestack = []

ipstack.append(99999)
timestack.append(float("inf"))

SOCKS_PORT = 7000
API_URL = "https://api.angel.co/1/users/%i"

socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', SOCKS_PORT)
socket.socket = socks.socksocket

def query(url):
	try:				# Uses urllib to fetch a site using SocksiPy for Tor over the SOCKS_PORT.
		return urllib.urlopen(url).read()
	except:
		return "Unable to reach %s gave up"% url

# def open_tor():						#sets up a new connection and tests the ip address
# 	exitcode = exits[random.randint(0,1)]
#   	tor_process = stem.process.launch_tor_with_config(
# 	    config = {
# 	      'SocksPort': str(SOCKS_PORT),
# 	      'ExitNodes': "{%s}" % exitcode ,
# 	    }
#     )
# 	ip = query("https://www.atagar.com/echo.php") #choke point**
# 	# ip = re.search('\d+\.\d+\.\d+\.\d+',ip) # regex is too slow on python
# 	# ip = ip.group(0)
# 	return ip

def open_vpn(): #a lot faster
	os.system('/opt/cisco/anyconnect/bin/vpn -s <connect.txt')
	ip = query("https://www.atagar.com/echo.php")
	return ip

def kill_vpn():
	os.system('/opt/cisco/anyconnect/bin/vpn -s disconnect')

def updatestack(): #removes ip addresses that are no longer blacklisted
	currenttime = time.time()
	if len(timestack)==1: #while it's empty
		return 0
	lasttime = timestack[1] #not empty
	while currenttime-lasttime >= 3600 and len(timestack)!=1:
		timestack.pop(1)	
		ipstack.pop(1)
		if len(timestack)!=1:
			lasttime=timestack[1]

# def newconnection():
# 	updatestack()
# 	ip = open_tor()
# 	while ip in ipstack:
# 		os.system("killall tor")
# 		ip = open_tor() #make sure we're not using the same ips within a single hour
# 		print "changing ip, because this one is still banned\n"
# 	ipstack.append(ip)
# 	timestack.append(time.time())
# 	print "switched up to %s\n" %ip

def newmcgillconnect():
	updatestack()
	ip = open_vpn()
	print ip
	if ip in ipstack:
		while ip in ipstack:
			kill_vpn()
			ip = open_vpn() #make sure we're not using the same ips within a single hour
			print "changing ip, because this one is still banned\n"
	ipstack.append(ip)
	timestack.append(time.time())
	print "switched up to %s\n" %ip

def mup():
	tic = 1
	response = ''
	update = 1 #update to match last 
	for i in range(update,778178): #max number of 778178 
		success = 0
		#while success == 0:
		try:
			if i == 1:
				newmcgillconnect() #start a whole new thing
			elif i % 900 ==0 or "Unable to reach" in response:	#reached the threshold where ban will be placed, or there was an issue with the last connection
				kill_vpn()
				newmcgillconnect()
			pingurl = API_URL % i
			response = query(pingurl) #choke point **
			success = 1
		except:
			print "failed to start tor, will pause and reset"
			time.sleep(10)
			kill_vpn()
			print "reset mcgill vpn...now process will begin again for %i" %i
			newmcgillconnect()
			success = 0
		if "investor\":true" in response:
		# if match: #if indeed an investor
			f = open("pages/%i.txt"%tic, 'w')
			f.write(response)
			f.close()
			print "finished id#%i\n"%i
			tic = tic+1
		else:
			print "tossed out id#%i\n"%i
# try:
# 	mup()
# except IOError:
# 	os.system("killall tor") #if it crahses
# 	mup()

# os.system("killall tor") #shutdown call
kill_vpn() #always make sure is dead
mup()