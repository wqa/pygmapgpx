#!/usr/local/bin/python3.6
#
# Example of cli tool using the GmapGpxClient-class
#
# usage:
#   ./gmapgpx.py 123456 "My nice route"
# will 
#   1. download route '123456' from gmap-pedometer
#   2. convert it into xml(gpx)-format
#   3. save it in 'My nice route.gpx'
#

import sys
from pygmapgpx import GmapGpxClient

dir = './'

client = GmapGpxClient()

sname = sys.argv.pop(0)

rId = 0
if len(sys.argv)>0:
    rId = int(sys.argv.pop(0))

rname = 'route_' + str(rId)
if len(sys.argv)>0:
    rname = sys.argv.pop(0)
    while len(sys.argv):
        rname += ' ' + sys.argv.pop(0)

status = 404
if rId > 0:
    status = client.get(rId)

if status == 200:
    try:
        fname = dir + rname + '.gpx'
        f = open(fname, "w")
        f.write(client.gpx(rname))
        f.close()
        print("OK, file",fname,"written")
    except:
        print("ERROR, file",fname,"couldn't be written:",sys.exc_info()[0])
else:
    print("rId=",rId,"status:",status)

