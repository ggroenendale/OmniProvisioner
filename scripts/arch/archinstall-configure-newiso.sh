#!/bin/bash

# This script is the initial step that runs within the archlinux live environment and makes
# sure archiso is installed, copies our scripts into it, then rebuilds the iso so that on 
# next boot with the newly packaged iso, arch linux will install and run all of our installation
# scripts

# Configs
OUTPUT_DIR=~/archiso-out
PROFILE_DIR=~/new-iso
CUSTOM_NAME=latest-custom-archlinux.iso
VENTOY_MOUNT=/mnt/ventoy

# First make sure that the archiso package is installed
pacman -S archiso

# This script assumes that a copy of the releng configuration from archiso is already copied
cp -r /usr/share/archiso/configs/releng ~/new-iso/

# We also want to make sure that we are working within the new_iso/ folder with this script
cd ~/new-iso

# And the Ventoy USB should be mounted with all of the scripts and configs.
#   lsblk -f  #Find the USB device name i.e. /dev/sdb
#   ls -l /dev/disk/by-id/
VENTOY_DEV="/dev/disk/by-id/usb-PNY_USB_3.1_FD_0700150D9DADBA90-0:0-part1"
# mkdir -p "$VENTOY_MOUNT"
# mount -t vfat -o rw,umask=000 "${VENTOY_DEV}-part1" "$VENTOY_MOUNT"

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

# Ensure that the live environment has the right version of archinstall ready.

if pacman -Qi archinstall 2>/dev/null | grep -E "^Version\s*:\s*3\.0\.8" >/dev/null; then
  echo "archinstall is version 3.0.8 (or 3.0.8-*)"
else
  echo "archinstall is NOT 3.0.8"
  
fi
pacman -Qi archinstall

# Copy the install script, python config, json config, and vault_pass to the airootfs/root/ folder
cp -r "$VENTOY_MOUNT/scripts/arch/arch_install.sh" "$PROFILE_DIR/airootfs/root/"
cp -r "$VENTOY_MOUNT/scripts/arch/install_arch.py" "$PROFILE_DIR/airootfs/root/"
cp -r "$VENTOY_MOUNT/scripts/arch/archconfig.json" "$PROFILE_DIR/airootfs/root/"
cp -r "$VENTOY_MOUNT/scripts/arch/password_encr.txt" "$PROFILE_DIR/airootfs/root/"
cp -r "$VENTOY_MOUNT/scripts/arch/password_user.txt" "$PROFILE_DIR/airootfs/root/"
cp -r "$VENTOY_MOUNT/.vault_pass.txt" "$PROFILE_DIR/airootfs/root/"

# Create the autoinstall service for the complete automated setup

create_autoinstall_service() {
    local airootfs_dir="$1"
    local exec_script="/root/arch_install.sh"

    mkdir -p "$airootfs_dir/etc/systemd/system/"

    cat <<EOF > "$airootfs_dir/etc/systemd/system/autoinstall.service"
[Unit]
Description=Automatic Arch Installer
After=network.target

[Service]
Type=oneshot
ExecStart=$exec_script

[Install]
WantedBy=multi-user.target
EOF

    echo "Created autoinstall.service in $airootfs_dir"
}

# Create the autoinstall.service file
create_autoinstall_service "$PROFILE_DIR/airootfs"

# Once these files are inside the airootfs then we should be able to repackage the iso
mkarchiso -v -o "$OUTPUT_DIR" "$PROFILE_DIR"

# Find the freshly built ISO
ISO=$(ls "$OUTPUT_DIR"/*.iso)

# Rename it
mv "$ISO" "$OUTPUT_DIR/$CUSTOM_NAME"

# Finally, copy the new-iso back onto the ventoy usb so it can be used in the next load.
cp "$OUTPUT_DIR/$CUSTOM_NAME" "$VENTOY_MOUNT/isos/Arch/"

