#!/bin/bash

# This script assumes that a copy of the releng configuration from archiso is already copied
#   cp -r /usr/share/archiso/configs/releng ~/new-iso

# And the Ventoy USB should be mounted with all of the scripts and configs.
#   lsblk -f  #Find the USB device name i.e. /dev/sdb
#   mkdir -p /mnt/ventoy
#   mount -t vfat -o rw,umask=000 /dev/sdb1 /mnt/ventoy
# Verify Mount
#   ls /mnt/ventoy  # Should show Ventoy files and ISO directory
#   df -h /mnt/ventoy  # Check free space

# Copy the install script, python config, json config, and vault_pass to the airootfs/root/ folder
cp -r /mnt/ventoy/scripts/arch/arch_install.sh ~/new-iso/airootfs/root/
cp -r /mnt/ventoy/scripts/arch/install_arch.py ~/new-iso/airootfs/root/
cp -r /mnt/ventoy/scripts/arch/archconfig.json ~/new-iso/airootfs/root/
cp -r /mnt/ventoy/.vault_pass.txt ~/new-iso/airootfs/root/
