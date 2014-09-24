import StringIO
import json
import socket
import urllib
import datetime
import re

import socks  # SockiPy module
import stem.process
from stem.util import term
from datetime import date

exits = ["us","ca","mx","jp","gb","kr","fr"]

ipstack = [] #stacks used to track the ip and time it was last banned
timestack = []


SOCKS_PORT = 7000
API_URL = "https://api.angel.co/1/users/%i"

socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', SOCKS_PORT)
socket.socket = socks.socksocket

def open_tor ():						#sets up a new connection and tests the ip address
	exitcode = exits[random.randint(0,5)]
  	tor_process = stem.process.launch_tor_with_config(
    config = {
      'SocksPort': str(SOCKS_PORT),
      'ExitNodes': "{%s}" % exitcode ,
    },
    )
    ip = query("https://www.atagar.com/echo.php")
	ip = re.search('\d+\.\d+\.\d+\.\d+',ip)
	ip = ip.group(0)
	return ip

def query(url):
  try:				# Uses urllib to fetch a site using SocksiPy for Tor over the SOCKS_PORT.
    return urllib.urlopen(url).read()
  except:
    return "Unable to reach %s" % url

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
		tor_process.kill()
		ip = open_tor() #make sure we're not using the same ips within a single hour
	ipstack.append(ip)
	timestack.append(time.time())

def fuckemup():
	for i in range(1,742618):
		if i ==1:
			newconnection() #start a whole new thing
		if i % 900 == 0:
			tor_process.kill() #kill last one
			newconnection()
		pingurl = 


