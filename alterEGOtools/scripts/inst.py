#!/usr/bin/env python
## { alterEGO Linux: "Open the vault of knowledge" } ----------------------- ##
##                                                                           ##
## alterEGOtools/scripts/installer.py                                        ##
##   created        : 2021-11-26 16:41:09 UTC                                ##
##   updated        : 2021-11-30 10:51:56 UTC                                ##
##   description    : Install alterEGO Linux.                                ##
## _________________________________________________________________________ ##

import argparse
import os

from alterEGOtools.lib import configuration
from alterEGOtools.lib import msg
from alterEGOtools.lib import pkgutils
from alterEGOtools.lib import sysutils

## [ MESSAGES ] ------------------------------------------------------------ ##

message = msg.Msg
foreground_blue = message.color('lightblue')
foreground_green = message.color('lightgreen')
format_bold = message.color('bold')
format_reset = message.color('reset')

## [ INSTALLER ] ----------------------------------------------------------- ##

class Installer:

    def __init__(self, mode):

        self.mode = mode

    def partition(self):

        ## [ CREATE PARTITION ]
        message.console(f"{foreground_green}[*]{format_reset} {format_bold}Creating and mounting the partition...", wait=0)
        partition = '''label: dos
                    device: /dev/sda
                    unit: sectors
                    sector-size: 512

                    /dev/sda1 : start=        2048, type=83, bootable
                    '''

        sysutils.execute(f"sfdisk /dev/sda", input=partition)

        ## [ FORMAT FILE SYSTEM ]
        message.console(f"{foreground_green}[*]{format_reset} {format_bold}Formating the file system...", wait=0)
        sysutils.execute(f"mkfs.ext4 /dev/sda1")

    def mount(self):

        ## [ MOUNT /dev/sda1 TO /mnt ]
        message.console(f"{foreground_green}[*]{format_reset} {format_bold}Mounting /dev/sda1 to /mnt...", wait=0)
        sysutils.execute(f"mount /dev/sda1 /mnt")

        ## [ CREATE ${HOME} ]
        message.console(f"{foreground_green}[*]{format_reset} {format_bold}Creating /home...", wait=0)
        os.mkdir('/mnt/home')

    def pkg_prep(self):

        ## Enable pacman parallel download
        pkgutils.enable_parallel_download()

        ## Few prep.
        sysutils.execute(f"rm -rf /var/lib/pacman/sync")
        sysutils.execute(f"curl -o /etc/pacman.d/mirrorlist 'https://archlinux.org/mirrorlist/?country=US&protocol=http&protocol=https&ip_version=4'")
        sysutils.execute(f"sed -i -e 's/\#Server/Server/g' /etc/pacman.d/mirrorlist")
        sysutils.execute(f"pacman -Syy --noconfirm archlinux-keyring")

    def pkg_install(self):

        ## Packages installation.
        message.console(f"{foreground_green}[*]{format_reset} {format_bold}Starting pacstrap...", wait=0)
        pkgs_list = ' '.join(pkgutils.packages_list('pacstrap', self.mode))

        message.console(f"{foreground_blue}[-]{format_reset} {format_bold}Will install:\n{pkgs_list}", wait=0)
        run_pacstrap = sysutils.execute(f"pacstrap /mnt {pkgs_list}")

        message.console(f"{foreground_blue}[-]{format_reset} {format_bold}Pacstrap exit code: {run_pacstrap.returncode}", wait=0)

        return run_pacstrap.returncode

    def fstab(self):

        message.console(f"{foreground_green}[*]{format_reset} {format_bold}Generating the fstab...", wait=0)
        sysutils.execute(f"genfstab -U /mnt >> /mnt/etc/fstab", shell=True)

    def chroot(self):

        message.console(f"{foreground_green}[*]{format_reset} {format_bold}Preparing arch-root...", wait=0)

        sysutils.execute(f'arch-chroot /mnt pip install git+https://github.com/alterEGOlinux/alterEGOtools.git')
        sysutils.execute(f'arch-chroot /mnt python -m alterEGOtools.scripts.installer --sysconfig {self.mode}')


## [ CLI ] ----------------------------------------------------------------- ##

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--install", type=str, choices=['bare', 'minimal', 'beast'], help="Install AlterEGO Linux.")
    parser.add_argument("--sysconfig", type=str, choices=['bare', 'minimal', 'beast'], help="Initiate the system configuration after the base install.")

    args = parser.parse_args()

    ## [ SYSTEM PREP ] ----------------------------------------------------- ##

    if args.install:
        mode = args.install
        message.console(f"{foreground_green}[*]{format_reset} {format_bold}This will install AlterEGO Linux in {mode} mode...", wait=0)

        installer = Installer(mode)

        ## [ PARTITION ]
        installer.partition()

        ## [ MOUNTING PARTITION ]
        installer.mount()

        ## [ PACSTRAP ]
        installer.pkg_prep()

        ## Temporary solution due to few failure.
        run_pacstrap = installer.pkg_install()
        while run_pacstrap != 0:
            if input(f"{foreground_blue}[-]{format_reset} {format_bold}Re-run pacstrap [Y/n]? {format_reset}").lower() in ['y', 'yes']:
                run_pacstrap = installer.pkg_install()
            else:
                break

        ## [ FSTAB ]
        installer.fstab()

        ## [ ARCH-CHROOT ]
        installer.chroot()

        ## [ ALL DONE ]
        ## Returning from chroot.
        all_done = input(f"{foreground_green}[*]{format_reset} {format_bold}Shutdown [Y/n]? ")
        if all_done.lower() in ['y', 'yes']:
            message.console(f"{foreground_blue}[-]{format_reset} {format_bold}Good Bye!", wait=0)
            try:
                sysutils.execute(f'umount -R /mnt')
                sysutils.execute(f'shutdown now') 
            except:
                sysutils.execute(f'shutdown now') 
        else:
            message.console(f"{foreground_blue}[-]{format_reset} {format_bold}Do a manual shutdown when ready.", wait=0)

    ## [ SYSTEM CONFIGURATION ] -------------------------------------------- ##

    if args.sysconfig:
        mode = args.sysconfig
        installer = Installer(mode)

        ## [ GIT REPOSITORIES ]
        installer.pull_git()

        # ( TIMEZONE & CLOCK )
        # installer.set_time()

        # ( LOCALE )
        # installer.set_locale()

        # ( NETWORK CONFIGURATION )
        # installer.set_network()

        # ( POPULATING /etc/skel )
        # installer.skel()

        # ( USERS and PASSWORDS )
        # installer.users()

        # ( SHARED RESOURCES )
        # installer.shared_resources()

        # ( SWAPFILE )
        # installer.swapfile()

        # ( AUR )
        # installer.aur()

        # ( GENERATING mandb )
        # installer.mandb()

        # ( SETTING JAVA DEFAULT )
        # installer.set_java()

        # ( BOOTLOADER )
        # installer.bootloader()

        # ( VIRTUALBOX SERVICES )
        # installer.vbox_services()

if __name__ == '__main__':
    main()

## FIN _____________________________________________________________ ¯\_(ツ)_/¯
