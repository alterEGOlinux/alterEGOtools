#!/usr/bin/env python

## { alterEGO Linux: "Open the vault of knowledge" } ----------------------- ##
##                                                                           ##
## alterEGOtools/msg.py                                                      ##
##   created        : 2021-10-26 22:53:54 UTC                                ##
##   updated        : 2021-10-26 22:54:05 UTC                                ##
##   description    : Set of system utilities                                ##
## _________________________________________________________________________ ##

class Msg:

    def color(color='white'):
        colors = {
            'reset': '\033[00m',
            'bold': '\033[1m',
            'underline': '\033[4m',
            'dim': '\033[2m',
            'strickthrough': '\033[9m',
            'blink': '\033[5m',
            'reverse': '\033[7m',
            'hidden': '\033[8m',
            'normal': '\033[0m',
            'black': '\033[30m',
            'red': '\033[31m',
            'green': '\033[32m',
            'orange': '\033[33m',
            'blue': '\033[34m',
            'purple': '\033[35m',
            'aqua': '\033[36m',
            'gray': '\033[37m',
            'darkgray': '\033[90m',
            'lightred': '\033[91m',
            'lightgreen': '\033[92m',
            'lightyellow': '\033[93m',
            'lightblue': '\033[94m',
            'lightpurple': '\033[95m',
            'lightaqua': '\033[96m',
            'white': '\033[97m',
            'default': '\033[39m',
            'bgblack': '\033[40m',
            'bgred': '\033[41m',
            'bggreen': '\033[42m',
            'bgorange': '\033[43m',
            'bgblue': '\033[44m',
            'bgpurple': '\033[45m',
            'bgaqua': '\033[46m',
            'bggray': '\033[47m',
            'bgdarkgray': '\033[100m',
            'bglightred': '\033[101m',
            'bglightgreen': '\033[102m',
            'bglightyellow': '\033[103m',
            'bglightblue': '\033[104m',
            'bglightpurple': '\033[105m',
            'bglightaqua': '\033[106m',
            'bgwhite': '\033[107m',
            'bgdefault': '\033[49m',
            }

        return colors.get(color)

    def console(message, wait=0):
        print(message + Msg.color('reset'))
        time.sleep(wait)

## FIN _____________________________________________________________ ¯\_(ツ)_/¯
