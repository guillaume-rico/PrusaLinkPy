
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
    
    # Delete a files on USB drive :
    prusaMini.delete("/5H30M_~1.GCO")
    
    # Transferring a file to the printer
    if not prusaMini.exists_gcode('FOLDER/test.gcode') :
        prusaMini.put_gcode('C:/AM/test.gcode', 'FOLDER/test.gcode')
    
    # List files on USB Drive :
    prusaMini.get_v1_files().json()["children"]
    
    # Print this file 
    prusaMini.post_print_gcode('/usb/test.gcode')
    

The library changed its name in May 2024. Before it was called prusaLink.
Prusa staff asked me to leave them the name.

# Change Log 

1.0.0 :

 - First Release
 
 
2.0.0 :

 - Support firmware 5.1.0
 - Added : 

 * get_v1_files
 * put_gcode
 * exists_gcode
 
2.0.1 :

 - Bug correction on put_gcode
 
2.0.1 :

 - added :

 * delete

#  Bugs present in Prusa MINI printer firmware 4.4.1:

 * There is no possibility to have the list of folders present in a directory
    * Solved in firmware 5
 * You cannot upload a gcode in a subfolder of the USB key
    * Solved in firmware 5
 * When the printer detects the end of the filament and it displays "Change Filament" the telemetry information is no longer good. Here is the information returned by the printer in this case:
 
    'telemetry': {'temp-bed': 0.0, 'temp-nozzle': 0.0, 'print-speed': 100, 'z-height': 0.0, 'material': '---'}
    
 * Still in the case of a filament change, the status information is incorrect:

    'state': {'text': 'Operational', 'flags': {'operational': True, 'paused': False, 'printing': False, 'cancelling': False, 'pausing': False, 'sdReady': False, 'error': False, 'closedOnError': False, 'ready': True, 'busy': False}


# Installing PrusaLinkPy and Supported Versions

PrusaLinkPy is available on pip :

    python -m pip install PrusaLinkPy

PrusaLinkPy officially supports Python 3.9+ with Prusa MINI printer firmware 5.1.0.


# API Reference

## Low Level Functions

[get_version()](https://github.com/guillaume-rico/PrusaLinkPy#prusalinkpyget_version---read-version-)

[get_printer()](https://github.com/guillaume-rico/PrusaLinkPy#prusalinkpyget_printer---get-printer-)

[get_job()](https://github.com/guillaume-rico/PrusaLinkPy#prusalinkpyget_job---get-job-)

[get_v1_files(remoteDir)]()

[get_recursive_v1_files(remoteDir)]()

[delete(remotePath)]()

[put_gcode(filePathLocal, remoteDir)]()

[exists_gcode(remotePath)]()

[post_print_gcode(remotePath)](https://github.com/guillaume-rico/PrusaLinkPy#prusalinkpypost_print_gcoderemotepath---print-gcode-on-usb-drive)


## High Level Functions 

rm(remotePath) 

rm is used to delete all files in a folder :

    prusaMini.rm()

Function to add to the library:

 - Function to send then print
 - Synchronizing a local folder to the printer


# User Guide

## PrusaLinkPy.get_version()

Read version :


    import PrusaLinkPy
    prusaMini = PrusaLinkPy.PrusaLinkPy("192.168.0.123", "8ojHKHGNuAHA2bM", port=8017)
    obj = prusaMini.get_version()
    obj.json()
    
Return something like :

    {'api': '2.0.0', 'server': '2.1.2', 'nozzle_diameter': 0.4, 'text': 'PrusaLink', 'hostname': '', 'capabilities': {'upload-by-put': True}}


## PrusaLinkPy.get_printer()

Get printer :

    import PrusaLinkPy
    prusaMini = PrusaLinkPy.PrusaLinkPy("192.168.0.123", "8ojHKHGNuAHA2bM")
    obj = prusaMini.get_printer()
    obj.json()
    
Return something like :

    {'telemetry': 
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
    
    
## PrusaLinkPy.get_v1_files( remoteDir = '/')

Get Files on USB Drive :

    import PrusaLinkPy
    prusaMini = PrusaLinkPy.PrusaLinkPy("192.168.0.123", "8ojHKHGNuAHA2bM")
    obj = prusaMini.get_v1_files()
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

    obj = prusaMini.get_v1_files(remoteDir = '/SUBFOLDER')

## PrusaLinkPy.get_recursive_v1_files( remoteDir = '/')

Get all files in a folder and subfolder.
Warning : return nested dict.

    import PrusaLinkPy
    prusaMini = PrusaLinkPy.PrusaLinkPy("192.168.0.123", "8ojHKHGNuAHA2bM")
    dictt = prusaMini.get_recursive_v1_files()
    
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


## PrusaLinkPy.put_gcode(remotePath) 

Send a file on USB Drive.
Can create a folder !
if ret.status_code = 409 -> Conflict : File already exists

    import PrusaLinkPy
    prusaMini = PrusaLinkPy.PrusaLinkPy("192.168.0.123", "8ojHKHGNuAHA2bM")
    status = prusaMini.put('C:/MTN/DEBOUCHAGE.gcode' , 'MTN/DEBOUCHAGE.gcode')
    
## PrusaLinkPy.exists_gcode(remotePath) 

Check if a file exists on USB drive. Return True or False

    import PrusaLinkPy
    prusaMini = PrusaLinkPy.PrusaLinkPy("192.168.0.123", "8ojHKHGNuAHA2bM")
    status = prusaMini.exists_gcode('/DEBOUC~1.GCO')

## PrusaLinkPy.post_print_gcode(remotePath) 

Print GCODE on USB Drive 

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

retrieve thumbnail 

    r = requests.get('http://192.168.0.123:8017/thumb/l/usb/TAVERN~1.GCO', headers=headers)


/api/settings


POST /api/job
**[Link to Buddy code](https://github.com/prusa3d/Prusa-Firmware-Buddy/blob/master/lib/WUI/link_content/prusa_link_api.cpp#L276)**

GET/POST /api/download 
**[Link to Buddy code](https://github.com/prusa3d/Prusa-Firmware-Buddy/blob/master/lib/WUI/link_content/prusa_link_api.cpp#L289)**


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

