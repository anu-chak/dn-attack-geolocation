#!/usr/bin/python

import sqlite3
import webbrowser 
import math

class maps:

	def __init__(self, centerLat, centerLng, zoom ):
		self.center = (float(centerLat),float(centerLng))
		self.zoom = int(zoom)
		self.paths = []
		self.clientlat = None
		self.clientlng= None
		self.destlat = None
		self.destlng=None
		
	def addclientpoint(self, lat, lng):
		self.clientlat= lat
		self.clientlng= lng
		
	def adddestpoint(self, lat, lng):
		self.destlat = lat
		self.destlng= lng
		
	#create the html file which include one google map and all points and paths
	def draw(self, htmlfile):
		f = open(htmlfile,'wb')
		f.write('<html>\n')
		f.write('<head>\n')
		f.write('<meta name="viewport" content="initial-scale=1.0, user-scalable=no" />\n')
		f.write('<meta http-equiv="content-type" content="text/html; charset=UTF-8"/>\n')
		f.write('<title>Google Maps - pygmaps </title>\n')
		f.write('<script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>\n')
		f.write('<script type="text/javascript">\n')
		f.write('\tfunction initialize() {\n')
		self.drawmap(f)
		self.drawpoints(f)
		#self.drawpaths(f,self.paths)
		f.write('\t}\n')
		f.write('</script>\n')
		f.write('</head>\n')
		f.write('<body style="margin:0px; padding:0px;" onload="window.settimeout(initialize(),1000)">\n')
		f.write('\t<div id="map_canvas" style="width: 100%; height: 100%;"></div>\n')
		f.write('</body>\n')
		f.write('</html>\n')		
		f.close()
	
	def drawpoints(self,f):
		conn = sqlite3.connect('DNSLog.db')
		print "Opened database successfully";
		rs=conn.execute('''SELECT * FROM ATTACK_LOC''')
		resultset=rs.fetchall()
		
		f.write('\t\tvar latlng;\n')
		f.write('\t\tvar markerlist=[];\n')
		f.write('\t\tvar markers=[];\n')
		f.write('\t\tvar iterator=0;\n')
		f.write('\t\tvar icon;\n')

		for r in resultset:
			print r[3]," ",r[4]," ",r[6]," ",r[7]

			f.write('\t\tlatlng = new google.maps.LatLng(%f, %f);\n'%(r[3],r[4]))
			f.write('\t\tmarkerlist.push(latlng);\n')
			f.write('\t\tlatlng = new google.maps.LatLng(%f, %f);\n'%(r[6],r[7]))
			f.write('\t\tmarkerlist.push(latlng);\n')
		
		f.write('\n')
		f.write('\t\tfor (var i = 0; i < markerlist.length; i++) {\n')
		f.write('\t\t\tsetTimeout(function() {\n')
		
		f.write('\t\t\timg = new google.maps.MarkerImage("http://maps.google.com/mapfiles/ms/micons/red-dot.png");\n')
		f.write('\t\t\tmarkers.push(new google.maps.Marker({\n')
		f.write('\t\t\ticon: img,\n')
		f.write('\t\t\t\tposition: markerlist[iterator],\n')
		f.write('\t\t\t\tmap: map,\n')	
		f.write('\t\t\t\tdraggable: false,\n')
		f.write('\t\t\t\tanimation: google.maps.Animation.DROP\n')
		f.write('\t\t\t}));\n')
		f.write('\t\t\titerator++;\n')
		
		f.write('\t\t\timg = new google.maps.MarkerImage("http://maps.google.com/mapfiles/ms/icons/green-dot.png");\n')
		f.write('\t\t\tmarkers.push(new google.maps.Marker({\n')
		f.write('\t\t\ticon: img,\n')
		f.write('\t\t\t\tposition: markerlist[iterator],\n')
		f.write('\t\t\t\tmap: map,\n')	
		f.write('\t\t\t\tdraggable: false,\n')
		f.write('\t\t\t\tanimation: google.maps.Animation.DROP\n')
		f.write('\t\t\t}));\n')
		f.write('\t\t\titerator++;\n')
		
		f.write('\t\t},i * 2000);\n')
		f.write('\t}\n')
	
	def drawmap(self, f):
		f.write('\t\tvar centerlatlng = new google.maps.LatLng(%f, %f);\n' % (self.center[0],self.center[1]))
		f.write('\t\tvar myOptions = {\n')
		f.write('\t\t\tzoom: %d,\n' % (self.zoom))
		f.write('\t\t\tcenter: centerlatlng,\n')
		f.write('\t\t\tmapTypeId: google.maps.MapTypeId.ROADMAP\n')
		f.write('\t\t};\n')
		f.write('\t\tvar map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);\n')
		f.write('\n')

if __name__ == "__main__":
	
	mymap = maps(37.428, -10, 2)
	mymap.draw('mymap.draw.html') 
	url = 'mymap.draw.html'
	webbrowser.open_new_tab(url) 
