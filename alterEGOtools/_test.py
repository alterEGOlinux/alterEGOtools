#!/usr/bin/env python

## { alterEGO Linux: "Open the vault of knowledge" } ----------------------- ##
##                                                                           ##
## alterEGOtools/test.py                                                     ##
##   created        : 2021-10-18 21:10:53 UTC                                ##
##   updated        : 2021-10-18 21:11:03 UTC                                ##
##   description    : test file for alterEGOtools module                     ##
## _________________________________________________________________________ ##

import sys
from . import sysutils

if sys.argv[1] == "install":
    sysutils.execute(f"bash ~/repositories/alterEGOlinux/alterEGOtools/test/count_to_100.bash", shell=True)
else:
    sys.exit()

