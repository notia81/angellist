import urllib
import os
import time
from datetime import date
import StringIO

API_URL = "https://api.angel.co/1/users/%i"
kill_vpn = '/opt/cisco/anyconnect/bin/vpn -s disconnect'

ipstack = [] #stacks used to track the ip and time it was last banned
timestack = []

ipstack.append(99999)
timestack.append(float("inf"))
def query(url):
	try:				# Uses urllib to fetch a site using SocksiPy for Tor over the SOCKS_PORT.
		return urllib.urlopen(url).read()
	except:
		return "Unable to reach %s gave up"% url
def get_status():
	os.system('/opt/cisco/anyconnect/bin/vpn -s state > state.txt')
	print "just got state\n"
	time.sleep(5)
	g = open ('state.txt','r')
	textwall = g.read()
	g.close()
	if ('state: Disconnected' in textwall and 'notice: Ready to connect.' in textwall):
		return 1
	else:
		return 0
def open_vpn(status): #a lot faster
	if status == 0:
		print "the vpn is already running shutting down to restart\n"
		os.system(kill_vpn)
		time.sleep(5)
	os.system('/opt/cisco/anyconnect/bin/vpn -s <connect.txt')
	print "just opened connection\n"
	ip = query("https://www.atagar.com/echo.php")
	print ip
	return ip

def updatestack(): #removes ip addresses that are no longer blacklisted
	currenttime = time.time()
	if len(timestack)==1: #while it's empty
		return 0
	lasttime = timestack[1] #not empty
	while currenttime-lasttime >= 3600 and len(timestack)!=1:
		print "cleared 1 ip from ip stack\n"
		timestack.pop(1)	
		ipstack.pop(1)
		if len(timestack)!=1:
			lasttime=timestack[1]
def newconnection(status):
	updatestack()
	ip = open_vpn(status)
	while 'Unable to reach' in ip:
		ip = open_vpn(0)
	ipstack.append(ip)
	timestack.append(time.time())

def crawl():
	matched = 1 #updated:
	start = 1 #updated:
	response = ''
	status = get_status()
	for i in range(start,778178):
		if i == start:
			newconnection(status)
		elif i % 900 == 0:
			print "time to switch\n"
			newconnection(0)
		pingurl = API_URL % i
		response = query(pingurl)
		print response
		if "investor\":true" in response:
		# if match: #if indeed an investor
			f = open("pages/%i.txt"%matched, 'w')
			f.write(response)
			f.close()
			print "finished id#%i\n"%i
			matched = matched+1
		else:
			print "tossed out id#%i\n"%i
crawl()
os.system(kill_vpn)

# os.system('/opt/cisco/anyconnect/bin/vpn -s <connect.txt')
# ip = query("https://www.atagar.com/echo.php")
# print ip
# i= 999
# pingurl = API_URL % i
# response = query(pingurl)
# print response
# os.system('/opt/cisco/anyconnect/bin/vpn -s disconnect')

