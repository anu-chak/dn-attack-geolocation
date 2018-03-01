#!/usr/bin/python

import re
import collections
import sqlite3
		
def time(match):
	patt = re.compile("(\d{2}[:]\d{2}[:]\d{2}[.]\d{6})")
	match = patt.search(f)
	if match:
		x=match.group()
		return x
		
def protocol(match):
	patt = re.compile("(IP)")
	match = patt.search(f)
	if match:
		x=match.group()
		return x
		
def clientport(cip):
	patt= re.compile("(\\.([0-9]+) >)")
	m= patt.search(cip)
	if m:
		cprt=m.group(2)
	else:
		cprt= "#"
	return cprt
def clientip1(match):
	patt = re.compile("(([a-zA-Z0-9.-]+) >)")
	match = patt.search(f)
	if match:
		x=match.group(2)
		return x
def clientip2(match):
	patt = re.compile("(([a-zA-Z0-9.-]+)\\.[0-9]+ >)")
	match = patt.search(f)
	if match:
		x=match.group(2)
		return x
		
def destport(match):
	patt = re.compile("(\\.([0-9]+)[:])")
	match = patt.search(f)
	if match:
		x=match.group(2)
	else:
	    x="#"
	return x
def destip1(match):
	patt = re.compile("(> ([A-Za-z0-9.\-_]+)[:])")
	match = patt.search(f)
	if match:
		x=match.group(2)
		return x
def destip2(match):
	patt = re.compile("(> ([A-Za-z0-9.\-_]+)(\\.([0-9]+)[:]))")
	match = patt.search(f)
	if match:
		x=match.group(2)
		return x
		
def dnsidnum(match):
	patt = re.compile("(: ([0-9]+)(\\+|\\*|\\-| ))")
	
	match = patt.search(f)
	if match:
		x=match.group(2)
		return x

def dnssymbol(match):
	patt = re.compile("(: ([0-9]+)(\\+|\\*|\\-| ))")
	match = patt.search(f)
	if match:
		x=match.group(3)
		if x==" ":
			x="#"
	else:
		x="#"
	return x

def nxdsearch(match):
	patt = re.compile("(NXDomain|ServFail)")
	match = patt.search(f)
	if match:
		x=match.group()
		return x
		
def querytype(match):
	patt = re.compile("(([0-9]+/[0-9]+/[0-9]+)|\+|\-|\*) ([A-Z]+(\?)?)")

	match = patt.search(f)
	
	if match:
		x=match.group(3)
	else:
	    x= "#"
	return x
		
def authrec(match):
	patt = re.compile("([0-9]+/[0-9]+/[0-9]+)")
	patt2= re.compile("\[[1][a][u]\]")
	match = patt.search(f)
	match2= patt2.search(f)
	if match:
		x=match.group()
	elif match2:
	    x=match2.group()
	else:
	    x="#"
	return x

def dnsname(match):
	patt = re.compile("(([A-Za-z0-9.\-_\?]{2,200})((\\,)|( \([0-9]+\)$)))")
	match = patt.search(f)
	if match:
		x=match.group(2)
	else:
	    x= "#"
	return x
		
conn = sqlite3.connect('DNSLog.db')
cur= conn.cursor()
print "Opened database successfully";
conn.execute('''DROP TABLE IF EXISTS TCPD_OUTPUT''')
print "Table dropped successfully";
conn.execute('''CREATE TABLE TCPD_OUTPUT
			   (TIME CHAR(13), 
				PROTOCOL CHAR(3), 
				CLIENT_IP CHAR(200), 
				CLIENT_PORT CHAR(10), 
				DEST_IP CHAR(200), 
				DEST_PORT CHAR(10), 
				DNS_ID CHAR(10), 
				DNS_SYM CHAR(2), 
				AUTH_REC CHAR(10), 
				QUERY_TYPE CHAR(10), 
				DNS_NAME CHAR(200))''')
				
file = open('dnslog3.txt', 'r')
print file
c=0

for f in file:
	f = f.strip()
	c= c+1
	
	timestamp= time(f)
	proto= protocol(f)
	
	cprt= clientport(f)
	if cprt=="#":
	    cip= clientip1(f)
	else:
	    cip= clientip2(f)
		
	dprt= destport(f)
	if dprt=="#":
		dip= destip1(f)
	else:
		dip= destip2(f)
	
	dnsid= dnsidnum(f)
	dnssym= dnssymbol(f)
	rec= authrec(f)
		
	qtype= querytype(f)
	dnsnm= dnsname(f)
	
	print c," ",timestamp," ",proto," ",cip," ",cprt," ",dip," ",dprt," ",dnsid,dnssym," ",rec," ",qtype," ",dnsnm	
	stmt='''INSERT INTO TCPD_OUTPUT (TIME, PROTOCOL, CLIENT_IP, CLIENT_PORT, DEST_IP, DEST_PORT, 
			DNS_ID, DNS_SYM, AUTH_REC, QUERY_TYPE, DNS_NAME) VALUES (?,?,?,?,?,?,?,?,?,?,?);'''
	cur.execute(stmt, (timestamp, proto, cip, cprt, dip, dprt, dnsid, dnssym, rec, qtype, dnsnm))
	conn.commit()
print "Table created successfully";
conn.close()
