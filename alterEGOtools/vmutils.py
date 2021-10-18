#!/usr/bin/env python

## { alterEGO Linux: "Open the vault of knowledge" } ----------------------- ##
##                                                                           ##
## alterEGOtools/vmutils.py                                                  ##
##   created        : 2021-10-18 21:10:53 UTC                                ##
##   updated        : 2021-10-18 21:11:03 UTC                                ##
##   description    : Virtual machines module                                ##
## _________________________________________________________________________ ##

import subprocess
import shlex

def detect_vm():

    #### Use `$ systemd-detect-virt`
    #... If VirtualBox will return 'oracle'.
    #... If not in VM, will return 'none'.

    detect = subprocess.run(shlex.split(f"systemd-detect-virt"), stdout=subprocess.PIPE)

    result = detect.stdout.strip().decode('UTF-8')

    if result == 'none':
        return (False, 'NOT_A_VIRTUAL_MACHINE')
    else:
        return (True, result)
