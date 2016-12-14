#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import cgi, urlparse
import urllib2
#from internal import *
from client import *

def getFunction(name):
    possibles = globals().copy()
    possibles.update(locals())
    method = possibles.get(name)
    if not method:
        #raise NotImplementedError("Method %s not implemented" % name)
	return None
    return method


def readFile(self):
    try:
        #Open the static file requested and send it
	filePath = HOME + sep + self.path
        f = open(filePath)
        self.send_response(200)
        self.send_header('Content-type',mimeType(self.path))
        self.end_headers()
        #self.wfile.write(f.read())
	sendFile(filePath, self.wfile)
        f.close()
    except IOError:
        self.send_error(404,'File Not Found: %s' % self.path)


class myHandler(BaseHTTPRequestHandler):
    global HOME, INDEX

    #Handler for the GET requests
    def do_GET(self):

	#remove '/' from beginning
	self.path = self.path[1:len(self.path)]

	#1st) process client side functions
	#syntax: procedure?param1=value1&param2=value2...

	if self.path.find("?") > -1:

	    params = {}	
	    procedure, paramsStr = self.path.split("?")
	    paramsItems = paramsStr.split("&")
	    for item in paramsItems:
	        key, value = item.split("=")
	        params[key] = urllib2.unquote(value)

	    resource = getFunction(procedure)

	    if resource == None:
		self.send_error(404,'Undefined procedure: %s' % procedure)	   
		return 

            try:
                data, headers, httpCode = resource(self,params)

		if httpCode == '': 
		    httpCode = 200
	        self.send_response(httpCode)

		if headers == {}: 
		    headers = {'Content-type':'text/html'}
	        for key in headers:
		    value = headers[key]
		    self.send_header(key,value)
		
		self.send_header('Content-length',len(data))
		self.end_headers()

		#self.wfile.write(data)
                sendString(data, self.wfile)

            except Exception as e:
                self.send_error(500,'%s ' % e)

	    return

	else:
	    #2nd) read local file

            if self.path == "":
                self.path = "" + INDEX
            readFile(self)

        return


    def do_POST(self):

	global MAX_BYTES
	#to return warning/error message for too big posting files we had to receive 1st all data!
	global RECEIVE

	length = int(self.headers.getheader('content-length'))
	if length > MAX_BYTES:
	    print "Abort POSTING: Content-length: %s > MAX_BYTES = %s" % (length, MAX_BYTES)
	    if RECEIVE:
	        #not reading socket will produce reset connection in browser
	        self.rfile.read(length)

                msg = "Files too big!"
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.send_header('Content-length',len(msg))
                self.end_headers()
                self.wfile.write(msg)
	    return

        enctype, boundary = cgi.parse_header(self.headers.getheader('content-type'))

        if enctype == 'multipart/form-data':
            postvars = cgi.parse_multipart(self.rfile, boundary)
        elif enctype == 'application/x-www-form-urlencoded':
            length = int(self.headers.getheader('content-length'))
	    postvars = urlparse.parse_qs(self.rfile.read(length), keep_blank_values=1)
        else:
            postvars = {}

	#remove '/' from beginning
	formAction = self.path[1:len(self.path)]

	#process client side functions
	try:
	    resource = getFunction(formAction)
	    data, headers, httpCode = resource(self,postvars)

            if httpCode == '':
                httpCode = 200
            self.send_response(httpCode)

            if headers == {}:
                headers = {'Content-type':'text/html'}
            for key in headers:
                value = headers[key]
                self.send_header(key,value)

            self.send_header('Content-length',len(data))
            self.end_headers()

            #self.wfile.write(data)
            sendString(data, self.wfile)

        except Exception as e:
            self.send_error(500,'%s ' % e)

        return


try:
    server = HTTPServer((HOST, PORT), myHandler)
    print 'Started httpserver on port ' , PORT
	
    #Wait forever for incoming htto requests
    server.serve_forever()

except KeyboardInterrupt:
    print '^C received, shutting down the web server'
    server.socket.close()
