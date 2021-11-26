#!/usr/bin/env python

## { alterEGO Linux: "Open the vault of knowledge" } ----------------------- ##
##                                                                           ##
## alterEGOtools/installer.py                                                ##
##   created        : 2021-06-05 00:03:38 UTC                                ##
##   updated        : 2021-10-27 11:38:00 UTC                                ##
##   description    : Install alterEGO Linux.                                ##
## _________________________________________________________________________ ##

#### https://bit.ly/2SlqWzt
#### https://tiny.cc/alterEGO

import argparse
from collections import namedtuple
import os
import shlex
import shutil
import subprocess
import sys
import threading

from . import msg
from . import sysutils

## [ GLOBAL VARIABLES ] ---------------------------------------------------- ##

gitTOOLS = 'https://github.com/fantomH/alterEGOtools.git'
gitEGO = 'https://github.com/fantomH/alterEGO.git'
usr_local = '/usr/local'
localTOOLS = f'{usr_local}/alterEGOtools'
localEGO = f'{usr_local}/alterEGO'

timezone = 'America/New_York'
hostname = 'pc1'
root_passwd = 'toor'
user = 'ghost'
user_passwd = 'password1'

pkgs = {
        'alsa-utils':               'nice',
        'arp-scan':                 'hack',
        'base':                     'minimal',
        'base-devel':               'minimal',
        'bash-completion':          'minimal',
        'bat':                      'nice',
        'bc':                       'minimal',
        'bind':                     'nice',
        'binwalk':                  'hack',
        'bleachbit':                'nice',
        'bpytop':                   'minimal',
        'brave-bin':                'aur-nice',
        'burpsuite':                'aur-hack',
        'cmatrix':                  'hack',
        'code':                     'nice',
        'cronie':                   'minimal',
        'dirbuster':                'aur-hack',
        'docker':                   'hack',
        'dos2unix':                 'minimal',
        'dunst':                    'minimal',
        'easy-rsa':                 'beast',
        'entr':                     'nice',
        'exfat-utils':              'nice',
        'feh':                      'nice',
        'ffmpeg':                   'nice',
        'firefox':                  'nice',
        'freerdp':                  'nice',
        'fzf':                      'minimal',
        'gimp':                     'nice',
        'git':                      'minimal',
        'gnu-netcat':               'hack',
        'go':                       'nice',
        'gobuster-git':             'aur-hack',
        'grc':                      'hack',
        'gromit-mpx-git':           'aur-nice',
        'grub':                     'minimal',
        'htop':                     'nice',
        'i3-gaps':                  'nice',
        'i3blocks':                 'nice',
        'imagemagick':              'nice',
        'inkscape':                 'nice',
        'inxi':                     'aur-nice',
        'john':                     'hack',
        'jq':                       'nice',
        'jre11-openjdk':            'hack',
        'libreoffice-fresh':        'nice',
        'librespeed-cli-bin':       'aur-nice',
        'linux':                    'minimal',
        'lynx':                     'minimal',
        'man-db':                   'minimal',
        'man-pages':                'minimal',
        'mariadb-clients':          'hack',
        'metasploit':               'hack',
        'mlocate':                  'nice',
        'mtools':                   'nice',
        'mtr':                      'hack',
        'net-tools':                'hack',
        'networkmanager':           'minimal',
        'nfs-utils':                'nice',
        'nikto':                    'hack',
        'nmap':                     'nice',
        'ntfs-3g':                  'nice',
        'openssh':                  'minimal',
        'openvpn':                  'beast',
        'p7zip':                    'minimal',
        'pandoc-bin':               'aur-nice',
        'pavucontrol':              'nice',
        'perl-image-exiftool':      'hack',
        'php':                      'hack',
        'polkit-gnome':             'nice',
        'postgresql':               'hack',
        'powershell-bin':           'aur-nice',
        'pptpclient':               'nice',
        'pulseaudio':               'nice',
        'pv':                       'nice',
        'python-beautifulsoup4':    'hack',
        'python-pandas':            'hack',
        'python-pip':               'minimal',
        'python-pyaml':             'hack',
        'python-rich':              'hack',
        'qrencode':                 'hack',
        'qterminal':                'hack',
        'qtile':                    'nice',
        'ranger':                   'nice',
        'remmina':                  'nice',
        'rsync':                    'minimal',
        'rustscan':                 'aur-hack',
        'screen':                   'nice',
        'screenkey':                'nice',
        'shellcheck':               'nice',
        'simple-mtpfs':             'aur-nice',
        'sqlitebrowser':            'hack',
        'sxiv':                     'nice',
        'tcpdump':                  'beast',
        'tesseract':                'hack',
        'tesseract-data-eng':       'hack',
        'tesseract-data-fra':       'hack',
        'thunar':                   'nice',
        'thunar-volman':            'nice',
        'tidy':                     'hack',
        'tk':                       'hack',
        'tmux':                     'minimal',
        'traceroute':               'hack',
        'transmission-gtk':         'nice',
        'tree':                     'minimal',
        'ufw':                      'minimal',
        'unrar':                    'minimal',
        'unzip':                    'minimal',
        'usbutils':                 'minimal',
        'vim':                      'minimal',
        'virtualbox-guest-utils':   'nice',
        'w3m':                      'nice',
        'wfuzz-git':                'aur-hack',
        'wget':                     'minimal',
        'whois':                    'hack',
        'wireshark-qt':             'hack',
        'xclip':                    'nice',
        'xcompmgr':                 'nice',
        'xdotool':                  'nice',
        'xfce4-terminal':           'nice',
        'xorg-server':              'nice',
        'xorg-xinit':               'nice',
        'xterm':                    'nice',
        'youtube-dl':               'nice',
        'zaproxy':                  'hack',
        'zathura':                  'nice',
        'zathura-pdf-mupdf':        'nice',
        'zbar':                     'hack',
        }

GitOption = namedtuple('GitOption', ['name', 'remote', 'local', 'mode'])
git_repositories = [
    GitOption('alterEGOtools', 'https://github.com/fantomH/alterEGOtools.git', '/usr/local/alterEGOtools', ['minimal', 'niceguy', 'beast']),
    GitOption('alterEGO', 'https://github.com/fantomH/alterEGO.git', '/usr/local/alterEGO', ['minimal', 'niceguy', 'beast'])
    ]

foreground_blue = msg.Msg.color('lightblue')
foreground_green = msg.Msg.color('lightgreen')
format_bold = msg.Msg.color('bold')
format_reset = msg.Msg.color('reset')

## [ UTIL FUNCTIONS ] ------------------------------------------------------ ##

def copy_recursive(src, dst):
    '''
    The src is the source root directory.
    The dest is the source root of the destination.
    ref. http://techs.studyhorror.com/d/python-how-to-copy-or-move-folders-recursively
    '''

    if not os.path.exists(dst):
        os.makedirs(dst)

    msg.Msg.console(f"{foreground_green}[*]{format_reset} {format_bold}Copying files to {dst}...", wait=0)

    for src_dir, dirs, files in os.walk(src):
        dst_dir = src_dir.replace(src, dst)
        if not os.path.exists(dst_dir):
            os.mkdir(dst_dir)
            msg.Msg.console(f"{foreground_blue}[-]{format_reset} {format_bold}Creating directory {dst_dir}.", wait=0)

        for f in files:
            src_file = os.path.join(src_dir, f)
            dst_file = os.path.join(dst_dir, f)
            msg.Msg.console(f"{foreground_blue}[-]{format_reset} {format_bold}Copying {dst_file}.", wait=0)

            if os.path.exists(dst_file):
                os.remove(dst_file)
            shutil.copy2(src_file, dst_file)


## { INSTALLER FUNCTIONS }_____________________________________________________

def packages(required_by, mode=None):

    if required_by == 'pacstrap':
        if mode == 'minimal':
            pkgs_list = [k for k, v in pkgs.items() if v in ['minimal']]
        elif mode == 'niceguy':
            pkgs_list = [k for k, v in pkgs.items() if v in ['minimal', 'nice']]
        elif mode == 'beast':
            pkgs_list = [k for k, v in pkgs.items() if v in ['minimal', 'nice', 'hack']]
    elif required_by == 'yay':
        if mode == 'niceguy':
            pkgs_list = [k for k, v in pkgs.items() if v in ['aur-nice']]
        elif mode == 'beast':
            pkgs_list = [k for k, v in pkgs.items() if v in ['aur-nice', 'aur-hack']]

    return pkgs_list

def shared_bin():
    #### Deploys applications.

    localEGO_bin = f"{localEGO}/bin"
    files = os.listdir(localEGO_bin)

    msg.Msg.console(f"{foreground_green}[*]{format_reset} {format_bold}Deploying application to /usr/local/bin...", wait=0)
    for f in files:
        msg.Msg.console(f"{foreground_blue}[-]{format_reset} {format_bold}{f}", wait=0)
        src = os.path.join(localEGO_bin, f)
        dst = os.path.join('/usr/local/bin', f)
        os.symlink(src, dst)

def shared_resources():
    ##### TODO: All file copying should be one functions.
    ##... recursive, copy, symlinks...

    ## [ bookmarks.db ]

    f = 'bookmarks.db'
    msg.Msg.console(f"{foreground_green}[*]{format_reset} {format_bold}Deploying {f} to /usr/local/share...", wait=0)
    src = os.path.join(localEGO, 'share', f)
    dst = os.path.join('/usr/local/share', f)
    os.symlink(src, dst)

def shared_reverse_shells():
    ###### Deploys reverse shells.

    if not os.path.exists('/usr/local/share/reverse_shells'):
        os.mkdir('/usr/local/share/reverse_shells')

    localEGO_reverse_shells = f"{localEGO}/share/reverse_shells"
    files = os.listdir(localEGO_reverse_shells)

    msg.Msg.console(f"{foreground_green}[*]{format_reset} {format_bold}Deploying application to /usr/local/share/reverse_shells...", wait=0)
    for f in files:
        msg.Msg.console(f"{foreground_blue}[-]{format_reset} {format_bold}{f}", wait=0)
        src = os.path.join(localEGO_reverse_shells, f)
        dst = os.path.join('/usr/local/share/reverse_shells', f)
        os.symlink(src, dst)

def shared_wordlists():
    #### Deploys wordlists.

    if not os.path.exists('/usr/local/share/wordlists'):
        os.mkdir('/usr/local/share/wordlists')

    localEGO_wordlists = f"{localEGO}/share/wordlists"
    files = os.listdir(localEGO_wordlists)

    msg.Msg.console(f"{foreground_green}[*]{format_reset} {format_bold}Deploying wordlists to /usr/local/share/wordlists...", wait=0)
    for f in files:
        msg.Msg.console(f"{foreground_blue}[-]{format_reset} {format_bold}{f}", wait=0)
        src = os.path.join(localEGO_wordlists, f)
        dst = os.path.join('/usr/local/share/wordlists', f)
        os.symlink(src, dst)

## [ CLASS: Installer ] ---------------------------------------------------- ##

class Installer:

    def __init__(self, mode):
        self.mode = mode

    def partition(self):
        ## [ CREATE PARTITION ]
        msg.Msg.console(f"{foreground_green}[*]{format_reset} {format_bold}Creating and mounting the partition...", wait=0)
        partition = '''label: dos
                    device: /dev/sda
                    unit: sectors
                    sector-size: 512

                    /dev/sda1 : start=        2048, type=83, bootable
                    '''

        sysutils.execute(f"sfdisk /dev/sda", input=partition)

        ## [ FORMAT FILE SYSTEM ]
        msg.Msg.console(f"{foreground_green}[*]{format_reset} {format_bold}Formating the file system...", wait=0)
        sysutils.execute(f"mkfs.ext4 /dev/sda1")

    def mount(self):
        ## [ MOUNT /dev/sda1 TO /mnt ]
        msg.Msg.console(f"{foreground_green}[*]{format_reset} {format_bold}Mounting /dev/sda1 to /mnt...", wait=0)
        sysutils.execute(f"mount /dev/sda1 /mnt")

        ## [ CREATE ${HOME} ]
        msg.Msg.console(f"{foreground_green}[*]{format_reset} {format_bold}Creating /home...", wait=0)
        os.mkdir('/mnt/home')

    def mod_pacman_conf(self):
        #### Enabling ParallelDownloads in pacman.conf
        pacman_conf = '/etc/pacman.conf'
        pacman_conf_bkp = pacman_conf + '.bkp'
        shutil.move(pacman_conf, pacman_conf_bkp)
        with open(pacman_conf_bkp, 'r') as fin:
            with open(pacman_conf, 'w') as fout:
                for line in fin.readlines():
                    if "#ParallelDownloads = 5" in line:
                        fout.write(line.replace("#ParallelDownloads = 5", "ParallelDownloads = 5"))
                    else:
                        fout.write(line)
        os.remove(pacman_conf_bkp)

    def pacstrap(self):

        sysutils.execute(f"rm -rf /var/lib/pacman/sync")
        sysutils.execute(f"curl -o /etc/pacman.d/mirrorlist 'https://archlinux.org/mirrorlist/?country=US&protocol=http&protocol=https&ip_version=4'")
        sysutils.execute(f"sed -i -e 's/\#Server/Server/g' /etc/pacman.d/mirrorlist")
        sysutils.execute(f"pacman -Syy --noconfirm archlinux-keyring")

        msg.Msg.console(f"{foreground_green}[*]{format_reset} {format_bold}Starting pacstrap...", wait=0)
        pkgs_list = ' '.join(packages('pacstrap', self.mode))
        msg.Msg.console(f"{foreground_blue}[-]{format_reset} {format_bold}Will install:\n{pkgs_list}", wait=0)
        run_pacstrap = sysutils.execute(f"pacstrap /mnt {pkgs_list}")
        msg.Msg.console(f"{foreground_blue}[-]{format_reset} {format_bold}Pacstrap exit code: {run_pacstrap.returncode}", wait=0)

        return run_pacstrap.returncode


    def fstab(self):
        msg.Msg.console(f"{foreground_green}[*]{format_reset} {format_bold}Generating the fstab...", wait=0)
        sysutils.execute(f"genfstab -U /mnt >> /mnt/etc/fstab", shell=True)

    def chroot(self):
        msg.Msg.console(f"{foreground_green}[*]{format_reset} {format_bold}Preparing arch-root...", wait=0)

        sysutils.execute(f'arch-chroot /mnt pip install git+https://github.com/alterEGOlinux/alterEGOtools.git')
        if self.mode == 'minimal':
            sysutils.execute(f'arch-chroot /mnt python -m alterEGOtools.installer --sysconfig minimal')
        elif self.mode == 'niceguy':
            sysutils.execute(f'arch-chroot /mnt python -m alterEGOtools.installer --sysconfig niceguy')
        elif self.mode == 'beast':
            sysutils.execute(f'arch-chroot /mnt python -m alterEGOtools.installer --sysconfig beast')

    def pull_git(self):

        msg.Msg.console(f"{foreground_green}[*]{format_reset} {format_bold}Fetching AlterEGO tools, config and other stuff...", wait=0)

        for g in git_repositories:
            if self.mode in g.mode:
                msg.Msg.console(f"{foreground_blue}[-]{format_reset} {format_bold}Pulling {g.remote}.", wait=0)
                if not os.path.isdir(g.local):
                    sysutils.execute(f"git clone {g.remote} {g.local}")
                else:
                    sysutils.execute(f"git -C {g.local} pull")

    def set_time(self):
        msg.Msg.console(f"{foreground_green}[*]{format_reset} {format_bold}Setting clock and timezone...", wait=0)

        os.symlink(f'/usr/share/zoneinfo/{timezone}', '/etc/localtime')
        sysutils.execute(f'timedatectl set-ntp true')
        sysutils.execute(f'hwclock --systohc --utc')

    def set_locale(self):
        msg.Msg.console(f"{foreground_green}[*]{format_reset} {format_bold}Generating locale...", wait=0)

        sysutils.execute(f'sed -i "s/#en_US.UTF-8/en_US.UTF-8/" /etc/locale.gen')
        with open('/etc/locale.conf', 'w') as locale_conf:
            locale_conf.write('LANG=en_US.UTF-8')
        os.putenv('LANG', 'en_US.UTF-8')
        sysutils.execute(f'locale-gen')

    def set_network(self):
        msg.Msg.console(f"{foreground_green}[*]{format_reset} {format_bold}Setting up network...", wait=0)

        with open('/etc/hostname', 'w') as etc_hostname:
            etc_hostname.write(hostname)
        with open('/etc/hosts', 'w') as etc_hosts:
            etc_hosts.write(f'''
                            127.0.0.1	localhost
                            ::1		localhost
                            127.0.1.1	{hostname}.localdomain	{hostname}
                            ''')

        msg.Msg.console(f"{foreground_blue}[-]{format_reset} {format_bold}Enabling NetworkManager daemon...", wait=0)
        sysutils.execute(f'systemctl enable NetworkManager.service')

    def skel(self):
        if self.mode == 'beast' or self.mode == 'niceguy':
            msg.Msg.console(f"{foreground_green}[*]{format_reset} {format_bold}Populating /etc/skel...", wait=0)
            src = f"{localEGO}/config/"
            dst = f"/etc/skel/"
            copy_recursive(src, dst)

    def users(self):
        msg.Msg.console(f"{foreground_green}[*]{format_reset} {format_bold}Configuring users and passwords...", wait=0)
        msg.Msg.console(f"{foreground_blue}[-]{format_reset} {format_bold}Setting password for root user.", wait=0)
        sysutils.execute(f"passwd", input=f'{root_passwd}\n{root_passwd}\n')

        if self.mode == 'beast' or self.mode == 'niceguy':
            msg.Msg.console(f"{foreground_blue}[-]{format_reset} {format_bold}Creating user {user}", wait=0)
            sysutils.execute(f"useradd -m -g users -G wheel,docker {user}") 
            msg.Msg.console(f"{foreground_blue}[-]{format_reset} {format_bold}Setting password for {user}", wait=0)
            sysutils.execute(f"passwd {user}", input=f"{user_passwd}\n{user_passwd}\n")

            msg.Msg.console(f"{foreground_blue}[-]{format_reset} {format_bold}Enabling sudoers for {user}", wait=0)
            sysutils.execute(f'sed -i "s/# %wheel ALL=(ALL) NOPASSWD: ALL/%wheel ALL=(ALL) NOPASSWD: ALL/" /etc/sudoers')

    def shared_resources(self):
        if self.mode == 'beast':
            msg.Msg.console(f"{foreground_green}[*]{format_reset} {format_bold}Deploying shared resources...", wait=0)
            shared_resources()
            shared_bin()
            shared_wordlists()
            shared_reverse_shells()
            # -- assets
            copy_recursive(os.path.join(localEGO, 'share', 'assets'), os.path.join(usr_local, 'share', 'assets'))
            # -- backgrounds
            copy_recursive(os.path.join(localEGO, 'share', 'backgrounds'), os.path.join(usr_local, 'share', 'backgrounds'))

    def swapfile(self):
        msg.Msg.console(f"{foreground_green}Creating a 1G swapfile...", wait=0)

        sysutils.execute(f"fallocate -l 1G /swapfile")
        os.chmod('/swapfile', 0o600)
        sysutils.execute(f"mkswap /swapfile")
        sysutils.execute(f"swapon /swapfile")

        with open('/etc/fstab', 'a') as swap_file:
            swap_file.write("/swapfile none swap defaults 0 0")

    def aur(self):
        if self.mode == 'niceguy' or self.mode == 'beast':
            msg.Msg.console(f"{foreground_green}[*]{format_reset} {format_bold}Installing YAY...", wait=0)
            sysutils.execute(f"git clone https://aur.archlinux.org/yay.git", cwd='/opt')
            sysutils.execute(f"chown -R {user}:users /opt/yay")
            sysutils.execute(f"su {user} -c 'makepkg -si --needed --noconfirm'", cwd='/opt/yay')

            msg.Msg.console(f"{foreground_green}[*]{format_reset} {format_bold}Installing AUR packages...", wait=0)
            pkgs_list = ' '.join(packages('yay', mode=self.mode))
            msg.Msg.console(f"{foreground_blue}[-]{format_reset} {format_bold}Will be installed:\n{pkgs_list}", wait=0)
            sysutils.execute(f"sudo -u {user} /bin/bash -c 'yay -S --noconfirm {pkgs_list}'")

    def mandb(self):
        msg.Msg.console(f"{foreground_green}[*]{format_reset} {format_bold}Generating mandb...", wait=0)
        sysutils.execute(f"mandb")

    def set_java(self):
        #### Burpsuite not running with java 16.
        #### Will need to install jre11-openjdk.
        #### $ sudo archlinux-java set java-11-openjdk

        if self.mode == 'beast':
            msg.Msg.console(f"{foreground_green}[*]{format_reset} {format_bold}Fixing Java...", wait=0)
            sysutils.execute(f"archlinux-java set java-11-openjdk")

    def bootloader(self):
        msg.Msg.console(f"{foreground_green}[*]{format_reset} {format_bold}Installing and configuring the bootloader...", wait=0)
        sysutils.execute(f'grub-install /dev/sda')
        sysutils.execute(f'grub-mkconfig -o /boot/grub/grub.cfg')

    def vbox_services(self):
        if self.mode == 'beast' or self.mode == 'niceguy':
            msg.Msg.console(f"{foreground_green}[*]{format_reset} {format_bold}Starting vbox service...", wait=0)
            sysutils.execute(f'systemctl start vboxservice.service')
            sysutils.execute(f'systemctl enable vboxservice.service')


class HackerLab:

    def __init__(self, mode):
        self.mode = mode

    def is_hacker(self):
        pass

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--install", type=str, choices=['minimal', 'niceguy', 'beast'], help="Install AlterEGO Linux.")
    parser.add_argument("--post-mount", type=str, choices=['minimal', 'niceguy', 'beast'], help="Run on /mnt.")
    parser.add_argument("--sysconfig", type=str, choices=['minimal', 'niceguy', 'beast'], help="Initiate the system configuration after the Installer.")
    parser.add_argument("--rerun", type=str, help="Until I figure out things...")

    args = parser.parse_args()

    ## [ SYSTEM PREP ] ----------------------------------------------------- ##

    if args.install:
        mode = args.install
        msg.Msg.console(f"{foreground_green}[*]{format_reset} {format_bold}This will install AlterEGO Linux in {mode} mode...", wait=0)

        installer = Installer(mode)

        ## ( PARTITION )
        installer.partition()

        ## ( MOUNTING PARTITION )
        installer.mount()

        ## ( PACMAN CONF )
        #### Modifies /etc/pacman.conf
        installer.mod_pacman_conf()

        ## ( PACSTRAP )
        #### Temporary solution due to few failure.
        run_pacstrap = installer.pacstrap()
        while run_pacstrap != 0:
            if input(f"{foreground_blue}[-]{format_reset} {format_bold}Re-run pacstrap [Y/n]? {format_reset}").lower() in ['y', 'yes']:
                run_pacstrap = installer.pacstrap()
            else:
                break

        ## ( FSTAB )
        installer.fstab()

        ## ( ARCH-CHROOT )
        installer.chroot()

        ## ( ALL DONE )
        #### Returning from chroot.
        all_done = input(f"{foreground_green}[*]{format_reset} {format_bold}Shutdown [Y/n]? ")
        if all_done.lower() in ['y', 'yes']:
            msg.Msg.console(f"{foreground_blue}[-]{format_reset} {format_bold}Good Bye!", wait=0)
            try:
                sysutils.execute(f'umount -R /mnt')
                sysutils.execute(f'shutdown now') 
            except:
                sysutils.execute(f'shutdown now') 
        else:
            msg.Msg.console(f"{foreground_blue}[-]{format_reset} {format_bold}Do a manual shutdown when ready.", wait=0)

    ## [ SYSTEM CONFIGURATION ] -------------------------------------------- ##

    if args.sysconfig:
        mode = args.sysconfig
        installer = Installer(mode)

        ## ( GIT REPOSITORIES )
        installer.pull_git()

        ## ( TIMEZONE & CLOCK )
        installer.set_time()

        ## ( LOCALE )
        installer.set_locale()

        ## ( NETWORK CONFIGURATION )
        installer.set_network()

        ## ( POPULATING /etc/skel )
        installer.skel()

        ## ( USERS and PASSWORDS )
        installer.users()

        ## ( SHARED RESOURCES )
        installer.shared_resources()

        ## ( SWAPFILE )
        installer.swapfile()

        ## ( AUR )
        installer.aur()

        ## ( GENERATING mandb )
        installer.mandb()

        ## ( SETTING JAVA DEFAULT )
        installer.set_java()

        ## ( BOOTLOADER )
        installer.bootloader()

        ## ( VIRTUALBOX SERVICES )
        installer.vbox_services()

    ## { TESTING }_____________________________________________________________

    if args.rerun:
        eval(args.rerun)

if __name__ == '__main__':
    main()

## FIN _____________________________________________________________ ¯\_(ツ)_/¯
