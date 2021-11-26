#!/usr/bin/env python

## { alterEGO Linux: "Open the vault of knowledge" } ----------------------- ##
##                                                                           ##
## alterEGOtools/sysutils.py                                                 ##
##   created        : 2021-11-10 11:42:58 UTC                                ##
##   updated        : 2021-11-10 11:43:07 UTC                                ##
##   description    : Default configuration.                                 ##
## _________________________________________________________________________ ##

import configuration
import subprocess

def get_pkg_info():
    for x in configuration.packages:
        pkg_name = x.name

        paru = subprocess.run(['paru', '-Si', pkg_name], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).stdout.decode('UTF-8').split('\n')

        if paru[0] == '':
            repository = 'N/A'
            description = 'N/A'
            url = 'N/A'
        else:
            repository = paru[0].split(':')[1].strip()
            description = paru[3].split(':')[1].strip()
            url = paru[5].replace('://', '.....').split(':')[1].strip().replace('.....', '://')
        
        print(f'''
<h2>{pkg_name}</h2>
  <pre class="_pkginfo">
{repository}/{pkg_name}
  description      : {description}
  url              : <a href="{url}" target="_blank">{url}</a>
  </pre>''')

get_pkg_info()

## FIN _____________________________________________________________ ¯\_(ツ)_/¯
