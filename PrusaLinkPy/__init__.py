#!/usr/bin/python

import requests
import json

class PrusaLinkPy:
    """Wrapper for the PrusaLinkPy API.
    https://github.com/prusa3d/Prusa-Firmware-Buddy/blob/master/lib/WUI/link_content/basic_gets.cpp
    """
    
    def __init__(self, host: str, api_key: str, port=80) -> None:
        """Initialize the PrusaLinkPy class."""
        self.host = host
        self.port = str(port)
        self.api_key = api_key
        self.headers = {'X-Api-Key': api_key}
        
    def get_version(self) :
        """Get the version."""
        r = requests.get('http://' + self.host + ':' + self.port + '/api/version', headers=self.headers)
        return r
        
    def get_printer(self) :
        """Get the printer."""
        r = requests.get('http://' + self.host + ':' + self.port + '/api/printer', headers=self.headers)
        return r
        
    def get_job(self) :
        """Get the job."""
        r = requests.get('http://' + self.host + ':' + self.port + '/api/job', headers=self.headers)
        return r
        
    def get_files(self, remoteDir = '/') :
        """
        List files on USB Drive.
        
        Test code :
        import PrusaLinkPy
        prusaMini = PrusaLinkPy.PrusaLinkPy("192.168.1.211", "44Da9wHhThmzFFJ")
        files = prusaMini.get_files().json()
        
        r = requests.get('http://192.168.1.211/api/files', headers=headers)
        """
        print("get_files is depreciated. Use get_v1_files")
        # was : r = requests.get('http://' + self.host + ':' + self.port + '/api/files?recursive=true', headers=self.headers)
        r = requests.get('http://' + self.host + ':' + self.port + '/api/files' + remoteDir, headers=self.headers)
        return r
        
        
    def get_v1_files(self, remoteDir = '/') :
        """
        List files and folder on USB Drive.
        
        Test code :
        import PrusaLinkPy
        prusaMini = PrusaLinkPy.PrusaLinkPy("192.168.1.211", "44Da9wHhThmzFFJ")
        files = prusaMini.get_v1_files().json()
        
        r = requests.get('http://192.168.1.211/api/v1/files/usb/', headers=headers)
        """
        # was : r = requests.get('http://' + self.host + ':' + self.port + '/api/files?recursive=true', headers=self.headers)
        r = requests.get('http://' + self.host + ':' + self.port + '/api/v1/files/usb' + remoteDir, headers=self.headers)
        return r
        
    def post_gcode(self, filePathLocal) :
        """
        Send a file on USB Drive.
        
        Test code :
        import PrusaLinkPy
        prusaMini = PrusaLinkPy.PrusaLinkPy("192.168.1.211", "44Da9wHhThmzFFJ")
        files = prusaMini.post_gcode('C:/SLF/Perso/brio/_exportUSB/MTN/DEBOUCHAGE.gcode')
        
        files.json()['refs']['resource']
        
        """
        fileContentBinary = {'file': open(filePathLocal,'rb')}
        # Marche aussi avec 
        #r = requests.post('http://' + self.host + ':' + self.port + '/api/files/local/', headers=self.headers, files=fileContentBinary )
        r = requests.post('http://' + self.host + ':' + self.port + '/api/files/usb/', headers=self.headers, files=fileContentBinary )
        return r
        
    def put_gcode(self, filePathLocal, remoteDir) :
        """
        Send a file on USB Drive.
        Can create a folder !
        
        if ret.status_code = 409 -> Conflict : File already exists
        
        Test code :
        import PrusaLinkPy
        prusaMini = PrusaLinkPy.PrusaLinkPy("192.168.1.211", "44Da9wHhThmzFFJ")
        files = prusaMini.put('C:/SLF/Perso/brio/_exportUSB/MTN/DEBOUCHAGE.gcode' , 'MTN/DEBOUCHAGE.gcode')
        
        """
        if "bgcode" in filePathLocal :
            fileContentBinary = {'file': open(filePathLocal,'rb')}
        else :
            fileContentBinary = {'file': open(filePathLocal,'r')}
            
        r = requests.put('http://' + self.host + ':' + self.port + '/api/v1/files/usb/' + remoteDir, headers=self.headers, data=fileContentBinary )
        return r
        
    def exists_gcode(self, remoteDir) :
        """
        test if file exists.
        If exists :
            ret.status_code = 200
        if not 
            ret.status_code = 404
            
        Test code :
        import PrusaLinkPy
        prusaMini = PrusaLinkPy.PrusaLinkPy("192.168.1.211", "44Da9wHhThmzFFJ")
        fileExist = prusaMini.exists_gcode('MTN/DEBOUCHAGE.gcode')
        
        
        """
        r = requests.head('http://' + self.host + ':' + self.port + '/api/v1/files/usb/' + remoteDir, headers=self.headers )
        
        if r.status_code == 200 :
            return True
        else :
            return False
        
    def post_print_gcode(self, remotePath) :
        """
        Print on USB Drive.
        
        Test code :
        import PrusaLinkPy
        prusaMini = PrusaLinkPy.PrusaLinkPy("192.168.1.211", "44Da9wHhThmzFFJ")
        files = prusaMini.post_print_gcode('/usb/DEBOUC~1.GCO')
        
        """
        payload = {'command': 'start'}
        r = requests.post('http://' + self.host + ':' + self.port + '/api/files' + remotePath, headers=self.headers, data=json.dumps(payload))
        return r
        
        
    def delete_gcode(self, filePathRemote) :
        """
            Delete gcode on USB drive
            
            Test code :
            import PrusaLinkPy
            prusaMini = PrusaLinkPy.PrusaLinkPy("192.168.1.211", "44Da9wHhThmzFFJ")
            ret = prusaMini.delete_gcode('/usb/DEBOUC~1.GCO').json()
        """
        r = requests.delete('http://' + self.host + ':' + self.port + '/api/files' + filePathRemote, headers=self.headers)
        return r
        
    def rm(self, filePathRemote = '/') :
        """
            Delete all files in a directory
            
            import requests
            headers = {'X-Api-Key': "U7N37h7WdTrYicA"}
            r = requests.get('http://192.168.0.123:8015/api/files/', headers=self.headers)
            
        """
        ret = self.get_files(remoteDir = filePathRemote)
        
        # Check if response is json 
        if "{" in ret.text :
            for filejson in ret.json()['files'][0]['children'] :
                print("Delete file : " + filejson["path"])
                self.delete_gcode( filejson["path"])
        else :
            return ret
        
        
# Utilisation :
# import PrusaLinkPy
# prusaMini = PrusaLinkPy.PrusaLinkPy("192.168.0.123", "8ojHKHGNuAHA2bM", port=8017)
# prusaMini = PrusaLinkPy.PrusaLinkPy("192.168.1.211", "44Da9wHhThmzFFJ")
# obj = prusaMini.get_version()