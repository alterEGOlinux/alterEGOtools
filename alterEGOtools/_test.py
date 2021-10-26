#!/usr/bin/env python

## { alterEGO Linux: "Open the vault of knowledge" } ----------------------- ##
##                                                                           ##
## alterEGOtools/test.py                                                     ##
##   created        : 2021-10-18 21:10:53 UTC                                ##
##   updated        : 2021-10-18 21:11:03 UTC                                ##
##   description    : test file for alterEGOtools module                     ##
## _________________________________________________________________________ ##

import argparse
import sys
from . import sysutils

arg_parser = argparse.ArgumentParser(prog='_test.py', description='For testing purpose.')
arg_parser.add_argument('--install', help='mode')

args = arg_parser.parse_args()

if args.install:
    sysutils.execute(f"sudo pacman -Syu | tee -a ~/tmp/testpy.log", shell=True)
else:
    sys.exit()

