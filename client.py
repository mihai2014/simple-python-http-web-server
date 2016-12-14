from internal import *

#Client side procedures
import time
import urllib2

backButton = """
<script>
function goBack() {
    window.history.back();
}
</script>
<br><br>
<button onclick=goBack()>Back to previous page</button>
"""

def echo1(self,params):

    if "medium" in params:
        medium = params["medium"]
    else:
	medium = None

    if medium == "js":
	endLine = "\r\n"
    else:
	endLine = "<br>"

    msg = "GET " + self.path + " " + self.request_version + endLine
    msg = msg + str(self.headers)

    #display medium is html
    if medium == None:
	msg = msg.replace("\r\n","<br>")

    msg = msg +  endLine + "[ (this is not a part of request) unquoted path is: " + urllib2.unquote(self.path) + " ]"

    if medium == None:
	msg = msg + backButton

    headers = {}
    return [msg, headers, 200]

def echo2(self,postvars):

    medium = None

    if 'medium' in postvars:
        medium = postvars['medium'][0]

    if medium == "js":
        endLine = "\r\n"
    else:
        endLine = "<br>"

    msg = "POST " + self.path + " " + self.request_version + endLine
    msg = msg + str(self.headers) + endLine

    #display medium is html
    if medium == None:
        msg = msg.replace("\r\n","<br>")

    msg = msg + "firstname = " + str(postvars['firstname'][0]) + endLine
    msg = msg + "lastname = " + str(postvars['lastname'][0]) + endLine

    #truncate files display up to 100 bytes
    if "file" in postvars:
	file = postvars['file'][0]
	if len(file) > 100:
	    file = file[0:100]
        msg = msg + "file = [" + file + "]" + endLine

    if "file0" in postvars:
        file = postvars['file0'][0]
        if len(file) > 100:
            file = file[0:100]
        msg = msg + "file = [" + file + "]" + endLine

    if medium == None:
        msg = msg + backButton

    headers = {}
    return [msg, headers, 200]

def time(self):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now

    headers = {}
    return [html, headers, 200]
