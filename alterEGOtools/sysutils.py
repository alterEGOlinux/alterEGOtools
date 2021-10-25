#!/usr/bin/env python

## { alterEGO Linux: "Open the vault of knowledge" } ----------------------- ##
##                                                                           ##
## alterEGOtools/sysutils.py                                                 ##
##   created        : 2021-10-21 19:20:50 UTC                                ##
##   updated        : 2021-10-21 19:21:00 UTC                                ##
##   description    : Set of system utilities                                ##
## _________________________________________________________________________ ##

from collections import namedtuple
import subprocess
import shlex

def execute(cmd, cwd=None, shell=False, text=True, input=None):

    if shell == True:
        cmd_list = cmd
    else:
        cmd_list = shlex.split(cmd)
    if input:
        input = input.encode()
        
    cmd_run = subprocess.run(cmd_list, cwd=cwd, shell=shell, input=input)

    CommandResults = namedtuple('CommandResults', ['returncode'])
    return CommandResults(cmd_run.returncode)

command = f"bash ../../test/count_to_100.bash"

## FIN _____________________________________________________________ ¯\_(ツ)_/¯
