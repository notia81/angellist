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


exits = ["us","ca","mx","jp","gb","kr","fr"]

ipstack = [] #stacks used to track the ip and time it was last banned
timestack = []


SOCKS_PORT = 7000
API_URL = "https://api.angel.co/1/users/%i"

socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', SOCKS_PORT)
socket.socket = socks.socksocket

def query(url):
  try:				# Uses urllib to fetch a site using SocksiPy for Tor over the SOCKS_PORT.
    return urllib.urlopen(url).read()
  except:
    return "Unable to reach %s" % url

def open_tor():						#sets up a new connection and tests the ip address
	#exitcode = exits[random.randint(0,5)]
	exitcode = "us"
  	tor_process = stem.process.launch_tor_with_config(
	    config = {
	      'SocksPort': str(SOCKS_PORT),
	      'ExitNodes': "{%s}" % exitcode ,
	    }
    )
	ip = query("https://www.atagar.com/echo.php")
	ip = re.search('\d+\.\d+\.\d+\.\d+',ip)
	ip = ip.group(0)
	return ip



def updatestack(): #removes ip addresses that are no longer blacklisted
	currenttime = time.time()
	if not timestack: #while it's empty
		return 0
	while currenttime-timestack[0] >= 3600:
		timestack.remove()
		ipstack.remove()

def newconnection():
	updatestack()
	ip = open_tor()
	while ip in ipstack:
		os.system("killall tor")
		ip = open_tor() #make sure we're not using the same ips within a single hour
		print "changing ip, because this one is still banned\n"
	ipstack.append(ip)
	timestack.append(time.time())
	print "switched up to %s\n" %ip

def fuckemup():
	tic = 1
	for i in range(1,20):
		if i == 1:
			newconnection() #start a whole new thing
		if i % 5 == 0:	#reached the threshold where ban will be placed	
			os.system("killall tor")
			newconnection()
		pingurl = API_URL % i
		response = query(pingurl)
		match = re.search('investor\":true',response)
		if match: #if indeed an investor
			f = open("pages/%i.txt"%tic, 'w')
			f.write(response)
			f.close()
			print "finished id#%i\n"%i
			tic = tic+1
fuckemup()
os.system("killall tor") #shutdown call

