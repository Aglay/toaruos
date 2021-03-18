#!/usr/bin/python3.6
"""
Migrate root
"""

import subprocess
import sys
import os
import shutil
import fcntl

if not os.getuid() == 0:
    print("You almost definitely don't want to be running this (and you can't be cause you're not root).")
    sys.exit(1)

# Figure out what root is
with open('/proc/cmdline','r') as f:
    cmdline = f.read()

if cmdline:
    cmdline = cmdline.split()
    args = {}
    for arg in cmdline:
        if "=" in arg:
            key, value = arg.split("=",1)
            args[key] = value
    if 'root' in args:
        print("Original root is:", args['root'])
    else:
        print("Don't know what root is, bailing.")
        sys.exit(1)

root = args.get('root')
root_type = args.get('root_type','ext2')
start = args.get('_start','')


print("Remounting root to /dev/base...")
subprocess.check_output(['mount',root_type,root,'/dev/base'])

print("Mounting blank tmpfs to /...")
subprocess.check_output(['mount','tmpfs','x','/'])

print("Migrating root...")
blacklist = ['lost+found']
for ent in os.listdir('/dev/base'):
    if ent in blacklist:
        continue
    if os.path.isdir(os.path.join('/dev/base',ent)):
        try:
            print(f"Copying {ent}...")
            shutil.copytree('/dev/base/'+ent,'/'+ent,symlinks=True)
        except:
            print("failed to make",ent)

if '/dev/ram' in root:
    print("Freeing ramdisk...")
    if ',' in root:
        root,_ = root.split(',',1)
    with open(root,'r') as f:
        fcntl.ioctl(f, 0x4001)

if start == '--single':
    os.execv('/bin/compositor',['compositor','--','/bin/terminal','-Fl'])
elif start == '--vga':
    os.execv('/bin/terminal-vga',['terminal-vga','-l'])
else:
    os.execv('/bin/compositor',['compositor','--',start])
