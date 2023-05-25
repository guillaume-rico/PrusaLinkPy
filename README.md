
PrusaLinkPy is a library to use the Prusa Link API.

The library makes it easy to use the prusa API in python. The library is based on Request.

Example of use :

    # Library import
    import PrusaLinkPy
    
    # Printer instantiation
    # IP : 192.168.0.123
    # API KEY : 8ojHKHGNuAHA2bM
    prusaMini = PrusaLinkPy.PrusaLinkPy("192.168.0.123", "8ojHKHGNuAHA2bM")
    
    # Get bed temperature
    getPrint = prusaMini.get_printer()
    
    # Display bed temperature
    print(getPrint.json()["telemetry"]["temp-bed"])
    
    # Delete all files on USB drive (rootdir) :
    prusaMini.rm()
    
    # Transferring a file to the printer
    prusaMini.post_gcode('C:/AM/test.gcode')
    
    # List files on USB Drive (root dir) :
    prusaMini.get_files('/').json()['files'][0]['children']
    
    # Print this file 
    prusaMini.post_print_gcode('/usb/test.gcode')
    

The library changed its name in May 2025. Before it was called prusaLink.
Prusa staff asked me to leave them the name.

#  Bugs present in Prusa MINI printer firmware 4.4.1:

 * There is no possibility to have the list of folders present in a directory
 * You cannot upload a gcode in a subfolder of the USB key
 * When the printer detects the end of the filament and it displays "Change Filament" the telemetry information is no longer good. Here is the information returned by the printer in this case:
 
    'telemetry': {'temp-bed': 0.0, 'temp-nozzle': 0.0, 'print-speed': 100, 'z-height': 0.0, 'material': '---'}
    
 * Still in the case of a filament change, the status information is incorrect:

    'state': {'text': 'Operational', 'flags': {'operational': True, 'paused': False, 'printing': False, 'cancelling': False, 'pausing': False, 'sdReady': False, 'error': False, 'closedOnError': False, 'ready': True, 'busy': False}


  

# Installing PrusaLinkPy and Supported Versions

PrusaLinkPy is available on pip :

    python -m pip install PrusaLinkPy

PrusaLinkPy officially supports Python 3.9+ with Prusa MINI printer firmware 4.4.1.


# API Reference

## Low Level Functions

[get_version()](https://github.com/guillaume-rico/PrusaLinkPy#prusalinkpyget_version---read-version-)

[get_printer()](https://github.com/guillaume-rico/PrusaLinkPy#prusalinkpyget_printer---get-printer-)

[get_job()](https://github.com/guillaume-rico/PrusaLinkPy#prusalinkpyget_job---get-job-)

[get_files(remoteDir)](https://github.com/guillaume-rico/PrusaLinkPy#prusalinkpyget_files-remotedir------get-files-on-usb-drive-)

[delete_gcode(remotePath)](https://github.com/guillaume-rico/PrusaLinkPy#prusalinkpydelete_gcoderemotepath---delete-a-file-on-usb-drive)

[post_gcode(path)](https://github.com/guillaume-rico/PrusaLinkPy#prusalinkpypost_gcodefilepathlocal---send-gcode)

[post_print_gcode(remotePath)](https://github.com/guillaume-rico/PrusaLinkPy#prusalinkpypost_print_gcoderemotepath---print-gcode-on-usb-drive)


## High Level Functions 

rm(remotePath) 

rm is used to delete all files in a folder :

    prusaMini.rm()

Function to add to the library:

 - Function to send then print
 - Synchronizing a local folder to the printer


# User Guide

## PrusaLinkPy.get_version() - Read version :


    import PrusaLinkPy
    prusaMini = PrusaLinkPy.PrusaLinkPy("192.168.0.123", "8ojHKHGNuAHA2bM", port=8017)
    obj = prusaMini.get_version()
    obj.json()
    
Return something like :

    {'api': '2.0.0', 'server': '2.1.2', 'text': 'PrusaLinkPy MINI', 'hostname': 'PMINI3'}


## PrusaLinkPy.get_printer() - Get printer :

    import PrusaLinkPy
    prusaMini = PrusaLinkPy.PrusaLinkPy("192.168.0.123", "8ojHKHGNuAHA2bM")
    obj = prusaMini.get_printer()
    obj.json()
    
Return something like :

    {'telemetry': 
        {'temp-bed': 29.1, 
        'temp-nozzle': 30.5, 
        'print-speed': 100, 
        'z-height': 120.1, 
        'material': 'PLA'},
     'temperature': {
        'tool0': {
            'actual': 30.5,
            'target': 0.0, 
            'display': 0.0, 
            'offset': 0}, 
        'bed': {
            'actual': 29.1,
            'target': 0.0,
            'offset': 0}
     },
     'state': {
        'text': 'Operational',
        'flags': {
            'operational': True, 
            'paused': False, 
            'printing': False, 
            'cancelling': False, 
            'pausing': False, 
            'sdReady': False, 
            'error': False, 
            'closedOnError': False, 
            'ready': True, 
            'busy': False}
        }
    }

## PrusaLinkPy.get_job() - Get job :

    import PrusaLinkPy
    prusaMini = PrusaLinkPy.PrusaLinkPy("192.168.0.123", "8ojHKHGNuAHA2bM")
    obj = prusaMini.get_job()
    obj.json()
    
Return something like :

    {
        "state":"Operational",
        "job": null,
        "progress": null
    }
    
    
## PrusaLinkPy.get_files( remoteDir = '/' ) - Get Files on USB Drive :

Warning : Return onlys files ! Not folder !

    import PrusaLinkPy
    prusaMini = PrusaLinkPy.PrusaLinkPy("192.168.0.123", "8ojHKHGNuAHA2bM")
    obj = prusaMini.get_files()
    filesRet = obj.json()
    filesRet
    
Return something like :

    {
        'files': 
            [
                {
                    'name': 'USB', 
                    'path': '/usb',
                    'display': 'USB', 
                    'type': 'folder', 
                    'origin': 'usb', 
                    'children': 
                        [
                            {
                                'name': 'DEBOUC~1.GCO',
                                'display': 'DEBOUCHAGE.gcode',
                                'path': '/usb/DEBOUC~1.GCO',
                                'origin': 'usb',
                                'refs': 
                                    {
                                        'resource': '/api/files/usb/DEBOUC~1.GCO', 
                                        'thumbnailSmall': '/thumb/s/usb/DEBOUC~1.GCO', 
                                        'thumbnailBig': '/thumb/l/usb/DEBOUC~1.GCO', 
                                        'download': '/usb/DEBOUC~1.GCO'
                                    }
                            }
                        ]
                }
            ]
    }

To get the list :

    filesRet["files"][0]["children"]
    
Workalso with subfolder

    obj = prusaMini.get_files(remoteDir = '/USB/SUBFOLDER/')

## PrusaLinkPy.delete_gcode(remotePath) - Delete a file on USB drive

    import PrusaLinkPy
    prusaMini = PrusaLinkPy.PrusaLinkPy("192.168.0.123", "8ojHKHGNuAHA2bM")
    obj = prusaMini.delete_gcode('/usb/DEBOUC~1.GCO')

Not tested in folder

## PrusaLinkPy.post_gcode(filePathLocal) - Send GCODE 

    import PrusaLinkPy
    prusaMini = PrusaLinkPy.PrusaLinkPy("192.168.0.123", "8ojHKHGNuAHA2bM")
    obj = prusaMini.post_gcode('C:\test.gcode')
    obj.json()
    
Return something like :

    {
        "name":"DEBOUCHAGE.gcode",
        "origin":"local",
        "size":821,
        "refs":
            {
            "resource":"/api/files/usb/DEBOUCHAGE.gcode",
            "thumbnailSmall":"/thumb/s/usb/DEBOUCHAGE.gcode",
            "thumbnailBig":"/thumb/l/usb/DEBOUCHAGE.gcode",
            "download":"/usb/DEBOUCHAGE.gcode"
        }
    }

Speed transfer (By Ethernet) :
83s for 4.5Mo -> 54ko/s 

## PrusaLinkPy.post_print_gcode(remotePath) - Print GCODE on USB Drive 

Warning : Printer LCD must be on main screen !

    import PrusaLinkPy
    mini111 = PrusaLinkPy.PrusaLinkPy("192.168.1.211", "44Da9wHhThmzFFJ")
    ret = mini111.post_print_gcode('/usb/DEBOUC~1.GCO')
    
File can be in sub folder . Add subfolder name after USB. Example :

    ret = mini111.post_print_gcode('/usb/SUB_FOLDER_1/DEBOUC~1.GCO')

If printer is not on main page, an error is generated by printer :

    ret.text
    "409: Conflict\n\nCan't start print now\n"


# API

API not implemented in my lib  : 

    r = requests.get('http://192.168.0.123:8017/api/files/usb/TAVERN~1.GCO', headers=headers)

retrieve thumbnail 

    r = requests.get('http://192.168.0.123:8017/thumb/l/usb/TAVERN~1.GCO', headers=headers)


/api/settings


POST /api/job
**[Link to Buddy code](https://github.com/prusa3d/Prusa-Firmware-Buddy/blob/master/lib/WUI/link_content/prusa_link_api.cpp#L276)**

GET/POST /api/download 
**[Link to Buddy code](https://github.com/prusa3d/Prusa-Firmware-Buddy/blob/master/lib/WUI/link_content/prusa_link_api.cpp#L289)**

# Change Log 

1.0.0 :

 - First Release


# Inspiration

An other lib : 

https://github.com/home-assistant-libs/PrusaLinkPy/blob/main/PrusaLinkPy/


Les commandes dans la mini :
https://github.com/prusa3d/Prusa-Firmware-Buddy/blob/master/lib/WUI/link_content/basic_gets.cpp



# Construire la lib

    py -m build

To upload to testpi repo :

    py -m twine upload --repository testpi dist/*

To upload to pypi repo :

    py -m twine upload dist/*


https://medium.com/analytics-vidhya/how-to-create-a-python-library-7d5aea80cc3f

