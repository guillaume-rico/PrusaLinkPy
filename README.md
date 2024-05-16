
PrusaLinkPy is a library to use the Prusa Link API.

The library makes it easy to use the prusa API in python. The library is based on Request.

Installation, update :

    pip install prusaLinkPy
    pip install prusaLinkPy -U

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
    
    # Delete a files on USB drive :
    prusaMini.delete("/5H30M_~1.GCO")
    
    # Transferring a file to the printer
    if not prusaMini.exists_gcode('FOLDER/test.gcode') :
        prusaMini.put_gcode('C:/AM/test.gcode', 'FOLDER/test.gcode')
    
    # List files on USB Drive :
    prusaMini.get_files().json()["children"]
    
    # Print this file 
    prusaMini.post_print_gcode('/usb/test.gcode')
    

The library changed its name in May 2024. Before it was called prusaLink.
Prusa staff asked me to leave them the name.

# Change Log 

## 2.2.1 :

Tab correction

## 2.2 :

  Version made by [enrgarci](https://github.com/enrgarci)
 - Update README.md
 - Modified [delete_job()](#prusalinkpydelete_job) to fix request from get to delete
 - added :
   - [pause_print()](#prusalinkpypause_print)
   - [resume_print()](#prusalinkpyresume_print)
   - [stop_print()](#prusalinkpystop_print)

## 2.1.1 :

 - Update README.md
 - added :
   - get_transfer
   - get_settings
 
## 2.1.0 :

 - Update README.md
 - added :
   - delete
   - [get_status()](#prusalinkpyget_status)
   - [get_storage()](#prusalinkpyget_storage)
   - [delete_job()](#prusalinkpydelete_job)
 
## 2.0.1 :

 - Bug correction on [put_gcode(filePathLocal, remoteDir, printAfterUpload = False, overwrite = False)](#prusalinkpyput_gcoderemotepath-printafterupload--false-overwrite--false)
 
## 2.0.0 :

 - Support firmware 5.1.0
 - Added : 
   - [get_files(remoteDir)](#prusalinkpyget_files-remotedir--)
   - [put_gcode(filePathLocal, remoteDir, printAfterUpload = False, overwrite = False)](#prusalinkpyput_gcoderemotepath-printafterupload--false-overwrite--false)
   - [exists_gcode(remotePath)](#prusalinkpyexists_gcoderemotepath)
 
## 1.0.0 :

 - First Release

# Installing PrusaLinkPy and Supported Versions

PrusaLinkPy is available on pip :

    python -m pip install PrusaLinkPy

PrusaLinkPy officially supports Python 3.9+ with Prusa printers (MINI, MK4 or XL) firmware 5.1.0.


# API Reference

## Low Level Functions

[get_version()](#prusalinkpyget_version)

[get_printer()](#prusalinkpyget_printer)

[get_job()](#prusalinkpyget_job)

[get_status()](#prusalinkpyget_status)

[get_storage()](#prusalinkpyget_storage)

[get_files(remoteDir)](#prusalinkpyget_files-remotedir--)

[delete(remotePath)](#prusalinkpydeleteremotepath)

[post_gcode(remotePath)](#prusalinkpyput_post_gcode)

[put_gcode(filePathLocal, remoteDir, printAfterUpload = False, overwrite = False)](#prusalinkpyput_gcoderemotepath-printafterupload--false-overwrite--false)

[exists_gcode(remotePath)](#prusalinkpyexists_gcoderemotepath)

[pause_print()](#prusalinkpypause_print)

[resume_print()](#prusalinkpyresume_print)

[stop_print()](#prusalinkpystop_print)

Not documented :
 * get_transfer
 * get_settings

For compatibility with old versions :

[delete_job()](#prusalinkpydelete_job)

## High Level Functions 

[get_recursive_files(remoteDir)](#prusalinkpyget_recursive_files-remotedir--)


# User Guide

## PrusaLinkPy.get_version()

Read version :


    import PrusaLinkPy
    prusaMini = PrusaLinkPy.PrusaLinkPy("192.168.0.123", "8ojHKHGNuAHA2bM", port=8017)
    obj = prusaMini.get_version()
    obj.json()
    
Return something like :

    {
        'api': '2.0.0', 
        'server': '2.1.2', 
        'nozzle_diameter': 0.4, 
        'text': 'PrusaLink', 
        'hostname': '', 
        'capabilities': 
        {
            'upload-by-put': True
        }
    }


## PrusaLinkPy.get_printer()

Get printer :

    import PrusaLinkPy
    prusaMini = PrusaLinkPy.PrusaLinkPy("192.168.0.123", "8ojHKHGNuAHA2bM")
    obj = prusaMini.get_printer()
    obj.json()
    
Waiting for Changing Filament :

    'link_state': 'ATTENTION' 
    'error': True
    
Return something like :

    {
        'telemetry': 
        {
            'temp-bed': 16.3,
            'temp-nozzle': 16.7,
            'print-speed': 100,
            'z-height': 82.0,
            'material': 'PLA'
        }, 
        'temperature': 
        {
            'tool0': 
            {
                'actual': 16.7,
                'target': 0.0,
                'display': 0.0,
                'offset': 0
            },
            'bed': 
            {
                'actual':16.3,
                'target': 0.0,
                'offset': 0
            }
        },
        'state': 
        {
            'text': 'Operational',
            'flags': 
            {
                'operational': True,
                'paused': False,
                'printing': False,
                'cancelling': False,
                'pausing': False,
                'error': False,
                'sdReady': False,
                'closedOnError': False,
                'ready': True,
                'busy': False
            }
        }
    }

## PrusaLinkPy.get_job()

Get job :

    import PrusaLinkPy
    prusaMini = PrusaLinkPy.PrusaLinkPy("192.168.0.123", "8ojHKHGNuAHA2bM")
    obj = prusaMini.get_job()
    obj.json()
    
Return something like :

    {
        "state":"Operational",
        "job": None,
        "progress": None
    }
    
## PrusaLinkPy.delete_job(job)

Delete a job. Job number is available with get_job() or get_status()

    import PrusaLinkPy
    prusaMini = PrusaLinkPy.PrusaLinkPy("192.168.0.123", "8ojHKHGNuAHA2bM")
    obj = prusaMini.delete_job("43")
    

## PrusaLinkPy.get_status()

Get job :

    import PrusaLinkPy
    prusaMini = PrusaLinkPy.PrusaLinkPy("192.168.0.123", "8ojHKHGNuAHA2bM")
    obj = prusaMini.get_status()
    obj.json()
    
Value of printer->state :

    IDLE (Main Screen)
    PRINTING
    FINISHED (Print finish, screen not on main screen)
    PAUSED (Pause by user, Print fan error)
    STOPPED (Print finish, stopped by user)
    ATTENTION (Filament Change)
    
Return something like :

    {
        "job":
        {
            "id":43,
            "progress":0.00,
            "time_remaining":120,
            "time_printing":143
        },
        "storage":
        {
            "path":"/usb/",
            "name":"usb",
            "read_only":false
        },
        "printer":
        {
            "state":"PRINTING",
            "temp_bed":57.3,
            "target_bed":0.0,
            "temp_nozzle":24.1,
            "target_nozzle":0.0,
            "axis_z":162.2,
            "flow":100,
            "speed":100,
            "fan_hotend":0,
            "fan_print":0
        }
    }
    
## PrusaLinkPy.get_storage()

Get job :

    import PrusaLinkPy
    prusaMini = PrusaLinkPy.PrusaLinkPy("192.168.0.123", "8ojHKHGNuAHA2bM")
    obj = prusaMini.get_storage()
    obj.json()
    
Return something like :

    {
        'storage_list': 
        [
            {
                'path': '/usb/', 
                'name': 'usb',
                'type': 'USB', 
                'read_only': False, 
                'available': True
            }
        ]
    }
    
## PrusaLinkPy.get_transfer()

Not Tested

Get job :

    import PrusaLinkPy
    prusaMini = PrusaLinkPy.PrusaLinkPy("192.168.0.123", "8ojHKHGNuAHA2bM")
    obj = prusaMini.get_transfer()
    obj.text
    
Return something like :

    TODO
    
## PrusaLinkPy.get_settings()

Completely useless

See here :

https://github.com/prusa3d/Prusa-Firmware-Buddy/blob/4bea923810302d654b932291ba324eaedff072fc/lib/WUI/link_content/prusa_link_api.cpp#L181C16-L181C16

Comment from Prusa Developper :

     // Some stubs for now, to make more clients (including the web page) happier.

Get job :

    import PrusaLinkPy
    prusaMini = PrusaLinkPy.PrusaLinkPy("192.168.0.123", "8ojHKHGNuAHA2bM")
    obj = prusaMini.get_transfer()
    obj.text
    
Return something like :

    {"printer": {}}
    
## PrusaLinkPy.get_files( remoteDir = '/')

Get Files on USB Drive :

    import PrusaLinkPy
    prusaMini = PrusaLinkPy.PrusaLinkPy("192.168.0.123", "8ojHKHGNuAHA2bM")
    obj = prusaMini.get_files()
    filesRet = obj.json()
    
Return something like :

    {
        'type': 'FOLDER', 
        'ro': False, 
        'name': 'usb', 
        'children': 
        [
        {
            'name': 'MTN', 
            'ro': False, 
            'type': 'FOLDER', 
            'm_timestamp': 1702628945, 
            'display_name': 'MTN'
        },
        {
            'name': 'S2_V2IS', 
            'ro': False, 
            'type': 'FOLDER', 
            'm_timestamp': 1702565182, 
            'display_name': 'S2_V2IS'
        }
        ]
    }
    
Workalso with subfolder

    obj = prusaMini.get_files(remoteDir = '/SUBFOLDER')

## PrusaLinkPy.get_recursive_files( remoteDir = '/')

Get all files (only gcode and bgcode) in a folder and subfolder.

Warning : return nested dict.


    import PrusaLinkPy
    prusaMini = PrusaLinkPy.PrusaLinkPy("192.168.0.123", "8ojHKHGNuAHA2bM")
    dictt = prusaMini.get_recursive_files()
    
    {
        'MTN': 
        {
            'CHGT_BUSE.gcode': '/MTN/CHGT_B~1.GCO', 
            'DEBOUCHAGE.gcode': '/MTN/DEBOUC~1.GCO', 
            'PRECHAUFFE.gcode': '/MTN/PRECHA~1.GCO'
        }, 
        'S2_V2IS': 
        {
            '2h33m.bgcode': '/S2_V2IS/2H33M~1.BGC',
            '5h5m.bgcode': '/S2_V2IS/5H5M~1.BGC'
        }
    }

## PrusaLinkPy.delete(remotePath) 

Delete a file or a folder on USB drive

    import PrusaLinkPy
    prusaMini = PrusaLinkPy.PrusaLinkPy("192.168.0.123", "8ojHKHGNuAHA2bM")
    obj = prusaMini.delete('/DEBOUC~1.GCO')


## PrusaLinkPy.post_gcode(remotePath) 

Print a file already poresent on USB key 

    import PrusaLinkPy
    prusaMini = PrusaLinkPy.PrusaLinkPy("192.168.0.123", "8ojHKHGNuAHA2bM")
    obj = prusaMini.post_gcode('/DEBOUC~1.GCO')

## PrusaLinkPy.put_gcode(remotePath, printAfterUpload = False, overwrite = False) 

Send a file on USB Drive.

Can create a folder !

if ret.status_code = 409 -> Conflict : File already exists
if ret.status_code = 415 -> {"title": "415: Unsupported Media Type","message":"Not a GCODE"}

printAfterUpload : Set at True to print after upload. 

overwrite : Allow file Overwrite

FW 5.1.0 :

 * Warning: printing starts even if the bed is not empty
 * Can only send bgcode and gcode
    

    import PrusaLinkPy
    prusaMini = PrusaLinkPy.PrusaLinkPy("192.168.0.123", "8ojHKHGNuAHA2bM")
    status = prusaMini.put('C:/MTN/DEBOUCHAGE.gcode' , 'MTN/DEBOUCHAGE.gcode')
    # Overwrite
    status = prusaMini.put('C:/MTN/DEBOUCHAGE.gcode' , 'MTN/DEBOUCHAGE.gcode', False, True)
    # Overwrite and Print
    status = prusaMini.put('C:/MTN/DEBOUCHAGE.gcode' , 'MTN/DEBOUCHAGE.gcode', True, True)
    
## PrusaLinkPy.exists_gcode(remotePath) 

Check if a file exists on USB drive. 

Return True or False

    import PrusaLinkPy
    prusaMini = PrusaLinkPy.PrusaLinkPy("192.168.0.123", "8ojHKHGNuAHA2bM")
    status = prusaMini.exists_gcode('/DEBOUC~1.GCO')

## PrusaLinkPy.pause_print() 

Pause actual print.

Added in 2.2.0 .

## PrusaLinkPy.resume_print() 

Resume paused print.

Added in 2.2.0 .

## PrusaLinkPy.stop_print() 

Stop actual print.

Added in 2.2.0 .

# API

API not implemented in my lib  : 

 * retrieve thumbnail :

    r = requests.get('http://192.168.0.123:8017/thumb/l/usb/TAVERN~1.GCO', headers=headers)

/api/settings


POST /api/job
**[Link to Buddy code](https://github.com/prusa3d/Prusa-Firmware-Buddy/blob/master/lib/WUI/link_content/prusa_link_api.cpp#L276)**

GET/POST /api/download 
**[Link to Buddy code](https://github.com/prusa3d/Prusa-Firmware-Buddy/blob/master/lib/WUI/link_content/prusa_link_api.cpp#L289)**


#  Bugs present in Prusa MINI printer firmware 4.4.1:

 * There is no possibility to have the list of folders present in a directory
    * Solved in firmware 5
 * You cannot upload a gcode in a subfolder of the USB key
    * Solved in firmware 5
 * When the printer detects the end of the filament and it displays "Change Filament" the telemetry information is no longer good. Here is the information returned by the printer in this case:
 
    'telemetry': {'temp-bed': 0.0, 'temp-nozzle': 0.0, 'print-speed': 100, 'z-height': 0.0, 'material': '---'}
    
 * Still in the case of a filament change, the status information is incorrect:

    'state': {'text': 'Operational', 'flags': {'operational': True, 'paused': False, 'printing': False, 'cancelling': False, 'pausing': False, 'sdReady': False, 'error': False, 'closedOnError': False, 'ready': True, 'busy': False}


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

