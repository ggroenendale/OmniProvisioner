#!/bin/bash

# This script is the initial step that runs within the archlinux live environment and makes
# sure archiso is installed, copies our scripts into it, then rebuilds the iso so that on 
# next boot with the newly packaged iso, arch linux will install and run all of our installation
# scripts

# First make sure that the archiso package is installed
pacman -S archiso

# This script assumes that a copy of the releng configuration from archiso is already copied
cp -r /usr/share/archiso/configs/releng ~/new-iso/

# We also want to make sure that we are working within the new_iso/ folder with this script
cd ~/new-iso

# And the Ventoy USB should be mounted with all of the scripts and configs.
#   lsblk -f  #Find the USB device name i.e. /dev/sdb
#
VENTOY_DEV="/dev/disk/by-id/usb-PNY_USB_3.1_FD_0700150D9DADBA90-0:0-part1"
mkdir -p /mnt/ventoy
mount -t vfat -o rw,umask=000 "${VENTOY_DEV}-part1" /mnt/ventoy

# Verify Ventoy Mount
echo "Checking /mnt/ventoy mount..."

# Get the output of the ls, then print if the command is successful or exit if not
if output=$(ls /mnt/ventoy 2>/dev/null); then  # Should show Ventoy files and ISO directory
    echo "Ventoy mount successful, Showing Contents:"
    echo "$output"
else
    echo "Error: Could not list /mnt/ventoy. Is it mounted?"
    exit 1
fi

# Copy the install script, python config, json config, and vault_pass to the airootfs/root/ folder
cp -r /mnt/ventoy/scripts/arch/arch_install.sh ~/new-iso/airootfs/root/
cp -r /mnt/ventoy/scripts/arch/install_arch.py ~/new-iso/airootfs/root/
cp -r /mnt/ventoy/scripts/arch/archconfig.json ~/new-iso/airootfs/root/
cp -r /mnt/ventoy/.vault_pass.txt ~/new-iso/airootfs/root/

# Once these files are inside the airootfs then we should be able to repackage the iso and then reboot...

