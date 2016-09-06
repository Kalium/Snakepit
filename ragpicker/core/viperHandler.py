# Copyright (C) 2013-2015 Ragpicker Developers.
# This file is part of Ragpicker Malware Crawler - http://code.google.com/p/malware-crawler/

import os
import json
import logging
import urllib
import urllib2

from core.config import Config
from utils.multiPartForm import MultiPartForm
from core.constants import RAGPICKER_ROOT

VIPER_URL_ADD = "http://%s:%s/file/add"
VIPER_URL_FIND = "http://%s:%s/file/find"

log = logging.getLogger("ViperHandler")

class ViperHandler():
    
    def __init__(self):
        self.cfgReporting = Config(os.path.join(RAGPICKER_ROOT, 'config', 'reporting.conf'))
        self.viperEnabled = self.cfgReporting.getOption("viper", "enabled")
        self.host = self.cfgReporting.getOption("viper", "host")
        self.port = self.cfgReporting.getOption("viper", "port")
        
        if not self.host or not self.port:
            raise Exception("Viper REST API server not configurated")
    
    def upload(self, filePath, fileName, tags):
        rawFile = open(filePath, 'rb')
        log.debug(VIPER_URL_ADD % (self.host, self.port) + " file=" + fileName)
        
        try:                
            form = MultiPartForm()
            form.add_file('file', fileName, fileHandle=rawFile)
            form.add_field('tags', tags)
            
            request = urllib2.Request(VIPER_URL_ADD % (self.host, self.port))
            body = str(form)
            request.add_header('Content-type', form.get_content_type())
            request.add_header('Content-length', len(body))
            request.add_data(body)
            
            response_data = urllib2.urlopen(request, timeout=60).read() 
            reponsejson = json.loads(response_data)           
            log.info("Submitted to Viper, message: %s", reponsejson["message"])   
        except urllib2.URLError as e:
            raise Exception("Unable to establish connection to Viper REST API server: %s" % e)
        except urllib2.HTTPError as e:
            raise Exception("Unable to perform HTTP request to Viper REST API server (http code=%s)" % e) 
        except ValueError as e:
            raise Exception("Unable to convert response to JSON: %s" % e)
        
        if reponsejson["message"] != 'added':
            raise Exception("Failed to store file in Viper: %s" % reponsejson["message"])
        
    # Exports malware file from the Viper using the sha256-hash
    def exportViper(self, sha256, exportDir):
        if os.path.isfile(exportDir + sha256):
            raise Exception("File %s already exists.") 
        
        cmd = "wget -q --tries=1 --directory-prefix=%s 'http://%s:%s/file/get/%s'" % (exportDir, self.host, self.port, sha256)
        os.system(cmd)
    
        if not os.path.isfile(exportDir + sha256):
            raise Exception("Download %s failed." % sha256)
        
    def isFileInCage(self, md5=None, sha256=None):
        if md5:
            param = { 'md5': md5 }
        elif sha256:
            param = { 'sha256': sha256 }
        
        request_data = urllib.urlencode(param)
    
        try:
            request = urllib2.Request(VIPER_URL_FIND % (self.host, self.port), request_data)
            response = urllib2.urlopen(request, timeout=60)
            response_data = response.read()
        except urllib2.HTTPError as e:
            if e.code == 400:
                # Error: 404 Not Found
                log.info('400 Invalid Search Term (' + str(param) + ')')
                return False
            else:
                raise Exception("Unable to perform HTTP request to Viper (http code=%s)" % e)
        except urllib2.URLError as e:    
            raise Exception("Unable to establish connection to Viper: %s" % e)  
        
        try:    
            check = json.loads(response_data)
        except ValueError as e:
            raise Exception("Unable to convert response to JSON: %s" % e)
            
        if md5:
            for i in check:
                if str(i) == "../":
                    return False
                if str(i) == "default":
                    for v in check[i]:
                        for d in v:
                            if str(d) == md5:
                                log.info("File " + md5 + " is in Viper")
                                return True
        elif sha256:
            for i in check:
                if str(i) == "../":
                    return False
                if str(i) == "default":
                    for v in check[i]:
                        for d in v:
                            if str(d) == sha256:
                                log.info("File " + sha256 + " is in Viper")
                                return True
        else:
            return False
