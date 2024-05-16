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
        """
        
            Get the version of the printer 
            Tested with mini and firmware 5
        
        """
        r = requests.get('http://' + self.host + ':' + self.port + '/api/version', headers=self.headers)
        return r
        
    def get_printer(self) :
        """
        
            Get the printer status
            Tested with mini and firmware 5
            
        """
        r = requests.get('http://' + self.host + ':' + self.port + '/api/printer', headers=self.headers)
        return r
        
    def get_job(self) :
        """
        
            Get the job.
            
        """
        r = requests.get('http://' + self.host + ':' + self.port + '/api/v1/job', headers=self.headers)
        return r

    def delete_job(self, job) :
        """
        
            Delete the job.
            
        """
        r = requests.delete('http://' + self.host + ':' + self.port + '/api/v1/job/' + str(job), headers=self.headers)
        return r
        
    def get_status(self) :
        """
        
            Get the status.
            
        """
        r = requests.get('http://' + self.host + ':' + self.port + '/api/v1/status', headers=self.headers)
        return r

    def get_storage(self) :
        """
        
            Get the storage.
            
        """
        r = requests.get('http://' + self.host + ':' + self.port + '/api/v1/storage', headers=self.headers)
        return r

    def get_transfer(self) :
        """
        
            Get the transfer
            
        """
        r = requests.get('http://' + self.host + ':' + self.port + '/api/v1/transfer', headers=self.headers)
        return r
        
    def get_settings(self) :
        """
        
            Get the settings
            
        """
        r = requests.get('http://' + self.host + ':' + self.port + '/api/settings', headers=self.headers)
        return r
        
    def get_files(self, remoteDir = '/') :
        """
        List files and folder on USB Drive.
        
        Test code :
        import PrusaLinkPy
        prusaMini = PrusaLinkPy.PrusaLinkPy("192.168.1.211", "44Da9wHhThmzFFJ")
        files = prusaMini.get_files().json()
        
        r = requests.get('http://192.168.1.211/api/v1/files/usb/', headers=headers)
        """
        # was : r = requests.get('http://' + self.host + ':' + self.port + '/api/files?recursive=true', headers=self.headers)
        r = requests.get('http://' + self.host + ':' + self.port + '/api/v1/files/usb' + remoteDir, headers=self.headers)
        return r
        
    def get_recursive_files(self, remoteDir = '/') :
        """
        List files and folder on USB Drive.
        
        Test code :
        import PrusaLinkPy
        prusaMini = PrusaLinkPy.PrusaLinkPy("192.168.1.211", "44Da9wHhThmzFFJ")
        files = prusaMini.get_files().json()
        
        """
        returnDict = {}
        
        if remoteDir[-1] != "/" :
            remoteDir = remoteDir + "/"
        
        ret = self.get_files(remoteDir)
        #print(ret.json()['children'])
        
        for filefolder in ret.json()['children'] :
            #print("work on" + str(filefolder))
            if filefolder['type'] == "FOLDER" :
                returnDict[filefolder['display_name']] = {}
                returnDict[filefolder['display_name']] = self.get_recursive_files(remoteDir + filefolder['display_name'] )
            elif filefolder['type'] == "PRINT_FILE" :
                returnDict[filefolder['display_name']] = remoteDir + filefolder['name']
        
        return returnDict
        
    def post_gcode(self, remotePath) :
        """
        Print a gcode
        
        Test code :
        import PrusaLinkPy
        prusaMini = PrusaLinkPy.PrusaLinkPy("192.168.1.211", "44Da9wHhThmzFFJ")
        files = prusaMini.post_gcode('/MTN/DEBOUCHAGE.gcode')
                
        """
        
        r = requests.post('http://' + self.host + ':' + self.port + '/api/v1/files/usb/' + remotePath, headers=self.headers,  )
        
        return r
        
    def put_gcode(self, filePathLocal, remoteDir, printAfterUpload = False, overwrite = False) :
        """
        Send a file on USB Drive.
        Can create a folder !
        
        if ret.status_code = 409 -> Conflict : File already exists
        
        Test code :
        import PrusaLinkPy
        prusaMini = PrusaLinkPy.PrusaLinkPy("192.168.1.211", "44Da9wHhThmzFFJ")
        files = prusaMini.put('C:/SLF/Perso/brio/_exportUSB/MTN/DEBOUCHAGE.gcode' , 'MTN/DEBOUCHAGE.gcode')
        
        Handmade :
        filePathLocal = 'C:/SLF/Perso/MyLittlePrusaFarm/groups/_COMMON/MTN/CHGT_BUSE.gcode'
        r = requests.put('http://192.168.0.144/api/v1/files/usb/CHGT_BUSE.gcode' , headers=headers, data=open(filePathLocal, 'rb') )
        
        """
        
        if overwrite :
            self.headers['Overwrite'] = "?1"
        if printAfterUpload :
            self.headers['Print-After-Upload'] = "?1"
        
        r = requests.put('http://' + self.host + ':' + self.port + '/api/v1/files/usb/' + remoteDir, headers=self.headers, data=open(filePathLocal, 'rb') )
        
        if overwrite :
            del self.headers['Overwrite']
        if printAfterUpload :
            del self.headers['Print-After-Upload']
        
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
        
    def delete(self, filePathRemote) :
        """
            Delete gcode on USB drive
            can delete a Folder !
            Test code :
            import PrusaLinkPy
            prusaMini = PrusaLinkPy.PrusaLinkPy("192.168.1.211", "44Da9wHhThmzFFJ")
            ret = prusaMini.delete_gcode('/usb/DEBOUC~1.GCO').json()
        """
        r = requests.delete('http://' + self.host + ':' + self.port + '/api/v1/files/usb' + filePathRemote, headers=self.headers)
        
        return r
        
    def delete_gcode(self, filePathRemote) :
        """
            Compatibility only
        """

        return self.delete(filePathRemote)
        
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
                self.delete( filejson["path"])
        else :
            return ret

    def pause_print(self) :
        """
        
            Pause job.
            None if no active job.
            
        """
        r = None
        job_info = self.get_job()
        # Check if response is json
        if "{" in job_info.text :
            if "id" in job_info.json():
                id = str(job_info.json()['id'])
                r = requests.put('http://' + self.host + ':' + self.port + '/api/v1/job/'+ id + '/pause', headers=self.headers)
        return r

    def resume_print(self) :
        """
        
            Resume current job.
            None if no active job.
            
        """
        r = None
        job_info = self.get_job()
        # Check if response is json 
        if "{" in job_info.text :
            if "id" in job_info.json():
                id = str(job_info.json()['id'])
                r = requests.put('http://' + self.host + ':' + self.port + '/api/v1/job/'+ id + '/resume', headers=self.headers)
        return r
    
    def stop_print(self) :
        """
        
            Stop current job.
            None if no active job
            
        """
        r = None
        job_info = self.get_job()
        # Check if response is json 
        if "{" in job_info.text :
            if "id" in job_info.json():
                id = str(job_info.json()['id'])
                r = requests.delete('http://' + self.host + ':' + self.port + '/api/v1/job/'+ str(id), headers=self.headers)
        return r

# Utilisation :
# import PrusaLinkPy
# prusaMini = PrusaLinkPy.PrusaLinkPy("192.168.0.123", "8ojHKHGNuAHA2bM", port=8017)
# prusaMini = PrusaLinkPy.PrusaLinkPy("192.168.1.211", "44Da9wHhThmzFFJ")
# obj = prusaMini.get_version()
