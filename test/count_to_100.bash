#!/usr/bin/env bash

## { alterEGO Linux: "Open the vault of knowledge" } ----------------------- ##
##                                                                           ##
## alterEGOtools/test/count_to_100.bash                                      ##
##   created        : 2021-10-22 22:26:33 UTC                                ##
##   updated        : 2021-10-22 22:26:41 UTC                                ##
##   description    : Simple script for testing                              ##
## _________________________________________________________________________ ##

  count=60
  while [[ ${count} -gt 0 ]]; do

    printf '%s\n' "${count}"
    ((count--))
    sleep 1 

  done

## FIN _____________________________________________________________ ¯\_(ツ)_/¯
