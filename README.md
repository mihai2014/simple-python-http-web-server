This is a simple httpserver based on BaseHTTPServer

0) Server coud handle GET and POST requests

1) In internal.py will be set the following parameters:

HOST = ''               #local host
PORT = 8000             #local port
CHUNK_SIZE = 128        #transmitting chunk size
HOME = 'www'            #local files directory
INDEX = "index.html"   #index file
MAX_BYTES = 5000000     #max nr of bytes allowed for posting
RECEIVE = False         #reset connection if content-length > max_bytes allowed for receiving

2) In client.py will be set client defined procedures. Example procedures(echo1, echo1) are set default an provide echo request features.
