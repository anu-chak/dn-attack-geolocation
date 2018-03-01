#!/usr/bin/python

import csv
import sqlite3
import sys
import re
import collections
import socket
import struct

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


def clientport(match):
	patt = re.compile("(\\.([0-9]+)[:])")
	match = patt.search(f)
	if match:
		x=match.group(2)
	else:
	    x="#"
	return x		
def clientip1(match):
	patt = re.compile("(> ([A-Za-z0-9.\-_]+)[:])")
	match = patt.search(f)
	if match:
		x=match.group(2)
		return x
def clientip2(match):
	patt = re.compile("(> ([A-Za-z0-9.\-_]+)(\\.([0-9]+)[:]))")
	match = patt.search(f)
	if match:
		x=match.group(2)
		return x
		
def querytype(match):
	patt = re.compile("(([0-9]+/[0-9]+/[0-9]+)|\+|\-|\*) ([A-Z]+(\?)?)")
	match = patt.search(f)
	if match:
		x=match.group(3)
	else:
	    x= "#"
	return x
	
def destip(match):   
	patt = re.compile("([A] ([0-9.]+))")
	match = patt.search(f)
	if match:
		x=match.group(2)
	else:
	    x= "#"
	return x
	
def ipconv(ip):
	ip.strip()
	parts=ip.split('.')
	sum=0
	count=3
	for part in parts:
		j=1
		p=1
		while j<=count:
			p=p*256
			j=j+1
		count= count-1
		sum= sum+p*int(part)
	return sum

#def ipconv(ip):
#	return struct.unpack("!I", socket.inet_aton(ip))[0]
	
conn = sqlite3.connect('DNSLog.db')
cur= conn.cursor()
print "Opened database successfully";

conn.execute('''DROP TABLE IF EXISTS ATTACK_LOC''')
conn.execute('''CREATE TABLE ATTACK_LOC
			   (DNS_ID NUMBER(10),
				DNS_SYM TEXT,
				CLIENT_IP TEXT,
			    CLIENT_LATITUDE NUMBER(20),
				CLIENT_LONGITUDE NUMBER(20),
				DEST_IP TEXT,
				DEST_LATITUDE NUMBER(20),
				DEST_LONGITUDE NUMBER(20),
				QUERY TEXT
				)''')
				
file = open('dnslog3.txt', 'r')
outfile= open('attackloc.txt','wb')
print file
c=0

for f in file:
	f = f.strip()
	c= c+1
	
	dnsid= dnsidnum(f)
	dnssym= dnssymbol(f)
	
	if dnssym=="#":
		#cprt= clientport(f)
		#if cprt=="#":
		#	cip= clientip1(f)
		#else:
		#	cip= clientip2(f)	
		
		cip= "127.0.0.1"
		cipnum= ipconv(cip)
		dip= destip(f)
		dipnum= ipconv(dip)

		stmt1= '''SELECT LATITUDE FROM GEO_IP WHERE IPNUM_START<=? AND IPNUM_END>=?'''
		stmt2= '''SELECT LONGITUDE FROM GEO_IP WHERE IPNUM_START<=? AND IPNUM_END>=?'''
		rs= conn.execute(stmt1,(cipnum,cipnum))
		clat=rs.fetchall()[0][0]
		rs= conn.execute(stmt2,(cipnum,cipnum))
		clng=rs.fetchall()[0][0]
		rs= conn.execute(stmt1,(dipnum,dipnum))
		dlat=rs.fetchall()[0][0]
		rs= conn.execute(stmt2,(dipnum,dipnum))
		dlng=rs.fetchall()[0][0]
		
		stmt= '''SELECT DNS_NAME FROM TCPD_OUTPUT WHERE DNS_ID=? AND DNS_SYM NOT IN ("#")'''
		rs= conn.execute(stmt, (dnsid,))
		query_name=rs.fetchall()[0][0]
		
		outfile.write(str(dnsid)+str(dnssym)+" "+str(cip)+" "+str(clat)+" "+str(clng)+" "+str(dip)+" "+str(dlat)+" "+str(dlng)+" "+str(query_name)+"\n")
		stmt='''INSERT INTO ATTACK_LOC (DNS_ID, DNS_SYM, CLIENT_IP, CLIENT_LATITUDE, CLIENT_LONGITUDE, 
				DEST_IP, DEST_LATITUDE, DEST_LONGITUDE, QUERY) VALUES (?,?,?,?,?,?,?,?,?)'''
		cur.execute(stmt, (dnsid, dnssym, cip, clat, clng, dip, dlat, dlng, query_name))
		print c," ",dnsid, dnssym," ",cip," ",clat," ",clng," ",dip," ",dlat," ",dlng," ",query_name
		conn.commit()

print "Table created successfully";
conn.close()
