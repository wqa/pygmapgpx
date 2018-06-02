#!/usr/local/bin/python3.6

import requests
from datetime import date
from datetime import timedelta
from datetime import datetime


class GmapGpxClient:
    config = {};

    def __init__(self):
        self.params = {}
        self.polyline = []
        self.points = []
        self.distance = 0
        self.name = ""
        self.rId = 0

    def get(self, rId):
        self.rId = rId
        self.rname = "Route " + str(self.rId)
        url = 'https://www.gmap-pedometer.com/gp/ajaxRoute/get'
        r = requests.post(url, data={'rId': self.rId})
        if r.status_code == 200:
            params = r.content.split(b'&')
            for param in params:
                if param.find(b'=')>0:
                    name,value = param.split(b'=')
                    self.params[name] = value
                    if name == b'polyline':
                        self.polyline = value.split(b'a')
            while len(self.polyline)>1:
                lat,long = float(self.polyline.pop(0)),float(self.polyline.pop(0))
                self.points.append([ lat, long ])
        return r.status_code

    def gpx(self, rname=''):
        if len(rname)>0:
            self.rname = rname
        result = '''<?xml version="1.0" encoding="UTF-8" ?>
<gpx version="1.1"
     creator="GmapGpxClient 1.0 - https://github.com/wqa/pygmapgpx"
     xmlns="http://www.topografix.com/GPX/1/1"
     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
     xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd">
   <rte>
      <name>{routename}</name>
      <cmt>Permalink: <![CDATA[ Permalink unavailable. ]]></cmt>  
'''.format(routename = self.rname)
        turnname = 'Start'
        turnnr = 0
        for point in self.points:
            result += '     <rtept lat="' + str(point[0]) +'" lon="' +str(point[1]) + '">' + "\n";
            result += '          <name>' + turnname + '</name>' + "\n"
            result += '     </rtept>' + "\n"
            turnnr += 1
            turnname = 'Turn ' + str(turnnr)

        result += '''   </rte>
</gpx>'''
        return result
