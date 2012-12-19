import httplib
import urllib
import mimetypes

from sugar.activity import activity

class HttpManager:

    def __init__(self, activity):
        self.host = "www.fing.edu.uy"
        self.reqFixedPath = "/grupos/medialab/xotoxo/"
        self._activity = activity

    def getId(self,id):
        print "HttpManager.getId"
        savedFile = "ERROR"
        # connecting to fing server and building the request with fake user-agent
        conn = httplib.HTTPConnection(self.host)
        req = self.reqFixedPath + "qrs.php?id="+str(id)
        
        try:
            conn.request("GET", req,"",{'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0','Host':'www.fing.edu.uy','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8'})        
        except:
            self._activity.playIt("sounds/error.wav")
        else:
            # getting response
            resp = conn.getresponse()
            if resp.status == 200:
                data = resp.read()
                # getting the filename to save the recived data with correct extension
                dispHeader = resp.getheader("content-disposition")
                if(dispHeader):
                    hSplit = dispHeader.split('/')
                    hSplitLen = len(hSplit)
                    fileName = hSplit[hSplitLen-1]
                    savedFile = "downloaded/"+fileName
                    fi=open(savedFile,"wb") 
                    fi.write(data)
                    fi.close() 
                    self._activity.act(savedFile)
                else:
                    self._activity.playIt("sounds/noContent.wav")    
            else:
                self._activity.playIt("sounds/error.wav")
        conn.close()
        print "[END]HttpManager.getId"

    def document_management_service(self,qrId,str_loc_file_path,*args):
        locfile = open(str_loc_file_path,'rb').read()
        host = self.host
        selector = self.reqFixedPath + "save.php"
        fields = [('id',qrId)]
        ext = str_loc_file_path.split('.')[-1]
        nameToSave =qrId+"."+ext
        files = [('uploadFile',nameToSave,locfile)]
        response = self.post_multipart(host, selector, fields, files)
        if response == "ERROR":
            self._activity.playIt("sounds/error.wav")
        else:
            self._activity.playIt("sounds/ready.wav")
        pass

    def post_multipart(self,host, selector, fields, files):
        content_type, body = self.encode_multipart_formdata(fields, files)
        try:
            h = httplib.HTTP(host)
            #h.set_debuglevel(1)
            h.putrequest('POST', selector)
            h.putheader('content-type', content_type)
            h.putheader('content-length', str(len(body)))
            h.putheader('User-Agent','Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0')
            h.putheader('Host', host)
            h.endheaders()
            h.send(body)
            errcode, errmsg, headers= h.getreply()
            return h.file.read()
        except:
            return "ERROR"

    def encode_multipart_formdata(self, fields, files):
        LIMIT = '----------lImIt_of_THE_fIle_eW_$'
        CRLF = '\r\n'
        L = []
        for (key, value) in fields:
            L.append('--' + LIMIT)
            L.append('Content-Disposition: form-data; name="%s"' % key)
            L.append('')
            L.append(value)
        for (key, filename, value) in files:
            L.append('--' + LIMIT)
            L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, str(filename)))
            L.append('Content-Type: %s' % self.get_content_type(filename))
            L.append('')
            L.append(value)
        L.append('--' + LIMIT + '--')
        L.append('')
        body = CRLF.join(L)
        content_type = 'multipart/form-data; boundary=%s' % LIMIT
        return content_type, body

    def get_content_type(self, filename):
        return mimetypes.guess_type(filename)[0] or 'application/octet-stream'
