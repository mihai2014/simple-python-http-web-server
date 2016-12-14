HOST = ''               #local host
PORT = 8000             #local port
CHUNK_SIZE = 128        #transmitting chunk size
HOME = 'www'            #local files directory
INDEX = "index.html"   #index file
MAX_BYTES = 5000000     #max nr of bytes allowed for posting
RECEIVE = False         #reset connection if content-length > max_bytes allowed for receiving

import os

#slicing sendig message in chunks to prevent truncating data
#in case of oversizing maximum amount of data that socket could handle

def sendFile(filePathSource,sockDestination):
    totalsent = 0
    size = str(os.stat(filePathSource).st_size)
    f = open(filePathSource,"rb")
    while totalsent < size:
        chunk = f.read(CHUNK_SIZE)
        sockDestination.write(chunk)
        sent = len(chunk)
        totalsent = totalsent + sent
        if(sent == 0): break
    f.close()

position = -1

def pull(string,chunk):
    global position

    start = position + 1
    end = position + chunk + 1
    position = end - 1

    return string[start : end]

#slicing sendig message in chunks to prevent truncating data
#in case of oversizing maximum amount of data that socket could handle

def sendString(strSource, sockDestination):
    global position
    totalsent = 0

    size = str(len(strSource))

    while totalsent < size:
        chunk = pull(strSource,CHUNK_SIZE)
        sockDestination.write(chunk)
        sent = len(chunk)
        totalsent = totalsent + sent
        if(sent == 0): break

    #reset contor
    position = -1


def mimeType(path):
    if path.endswith(".html"):
        mimetype='text/html'
    elif path.endswith(".js"):
        mimetype='application/javascript'
    elif path.endswith(".css"):
        mimetype='text/css'

    elif path.endswith(".jpg"):
        mimetype='image/jpg'
    elif path.endswith(".gif"):
        mimetype='image/gif'
    elif path.endswith(".ico"):
        mimetype='image/x-icon'
    elif path.endswith(".png"):
        mimetype='imge/png'

    elif path.endswith(".pdf"):
        mimetype='application/pdf'
    elif path.endswith(".txt"):
        mimetype='text/plain'
    elif path.endswith(".doc"):
        mimetype='application/msword'

    else:
        mimetype = 'application/octet-stream'

    return mimetype


#def isThere(string,keySearch):
#    params = {}
#    items = string.split("&")
#
#    for item in items:
#        key, value = item.split("=")
#        params[key] = value
#
#    if keySearch in params:
#        return params[key]
#    else:
#        return None







