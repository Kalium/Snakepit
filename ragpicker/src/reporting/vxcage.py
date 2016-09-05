# Copyright (C) 2013-2015 Ragpicker Developers.
# This file is part of Ragpicker Malware Crawler - http://code.google.com/p/malware-crawler/

from UserString import MutableString
import logging

from core.viperHandler import ViperHandler
from core.abstracts import Report

try:
    from yapsy.IPlugin import IPlugin
except ImportError:
    raise ImportError, 'Yapsy (Yet Another Plugin System) is required to run this program : http://yapsy.sourceforge.net'

log = logging.getLogger("ReportingViper")

class Viper(IPlugin, Report):
    """Viper is a Python application for managing a malware samples repository.
    """
    
    def run(self, results, objfile):
        self.key = "Viper"
        viper = ViperHandler()
        
        if objfile.file.is_permittedType():
            # Save file
            if viper.isFileInCage(md5 = objfile.file.get_fileMd5()) == False:
                fileName = objfile.file.get_fileMd5() + '.' + objfile.file.file_extension()
                viper.upload(objfile.file.temp_file, fileName, self._getTags(results, objfile.file))
                
            # Save unpacked file
            if objfile.unpacked_file and \
                viper.isFileInCage(md5 = objfile.unpacked_file.get_fileMd5()) == False:
                fileName = objfile.unpacked_file.get_fileMd5() + '.' + objfile.unpacked_file.file_extension()
                viper.upload(objfile.unpacked_file.temp_file, fileName, self._getTags(results, objfile.unpacked_file))
                
            # Save included files
            if len(objfile.included_files) > 0:
                for incl_file in objfile.included_files:
                    if viper.isFileInCage(md5 = incl_file.get_fileMd5()) == False:
                        fileName = incl_file.get_fileMd5() + '.' + incl_file.file_extension()
                        viper.upload(incl_file.temp_file, fileName, self._getTags(results, incl_file))
    
    def _getTags(self, results, file):
        tags = MutableString()
        
        # Digital Signature
        # isProbablyPacked
        try:
            if results["Info"] and results["Info"]["file"]:
                tags += results["Info"]["file"]["digitalSignature"]
                tags += ", "
                tags += "isProbablyPacked: " + str(results["Info"]["file"]["isProbablyPacked"])
                tags += ", "
        except KeyError:
            # Key is not present
            pass

        # URL
        if results["Info"] and results["Info"]["url"]:
            tags += results["Info"]["url"]["hostname"]
            tags += ", "
        
        # Packer Ident
        if results.get("PEID", None):
            tags += results["PEID"][0]
            tags += ", "
    
        # VirusTotal
        try:
            if results["VirusTotal"] and results["VirusTotal"]["file"] and results["VirusTotal"]["file"]["positives"]:
                tags += "VirusTotal: "
                tags += results["VirusTotal"]["file"]["positives"]
                tags += "/"
                tags += results["VirusTotal"]["file"]["total"]
                tags += ", "
        except KeyError:
            # Key is not present
            pass
        
        # CountryCode
        try:
            if results["InetSourceAnalysis"] and results["InetSourceAnalysis"]["URLVoid"]:
                tags += results["InetSourceAnalysis"]["URLVoid"]["urlResult"][1]["CountryCode"]
                tags += ", "
        except KeyError:
            # Key is not present
            pass
        
        # FileType
        tags += file.get_type()
        tags += ", "
                
        tags += "ragpicker"
        
        #TODO: Unpacked Tag einfuegen!!! 
        
        log.info("tags=" + tags)
        
        return str(tags)
