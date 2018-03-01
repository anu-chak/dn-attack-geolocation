#!/usr/bin/python
import csv
import sqlite3
import sys

conn = sqlite3.connect('DNSLog.db')
cur= conn.cursor()
print "Opened database successfully";

conn.execute('''DROP TABLE IF EXISTS GEO_IP''')
conn.execute('''CREATE TABLE GEO_IP
			   (IPNUM_START NUMBER(16),
			    IPNUM_END NUMBER(16),
				COUNTRY_CODE CHAR(3),
				COUNTRY CHAR(20),
				STATE CHAR(20),
				CITY CHAR(20),
				LATITUDE NUMBER(20),
				LONGITUDE NUMBER(20),
				ZIPCODE NUMBER(7),
				GMT CHAR(5),
				PRIMARY KEY(IPNUM_END))''')

stmt= '''INSERT INTO GEO_IP (IPNUM_START, IPNUM_END, COUNTRY_CODE, COUNTRY, STATE, CITY, LATITUDE, LONGITUDE, ZIPCODE, GMT)
         VALUES (?,?,?,?,?,?,?,?,?,?)'''
csv_file=csv.DictReader(open("ip2location-lite-db11.csv"))
for row in csv_file:
	cur.execute(stmt, (row["ipnumstart"],row["ipnumend"], row["countrycode"], row["country"], row["state"], row["city"], row["latitude"], row["longitude"], row["zipcode"], row["gmt"]))
	print row
	
conn.commit()
conn.close()
