# Omni Provisioner

Omni as in all devices

Provisioner as in this repository will be used to provision and configure all of my devices.

## Introduction

The purpose of this repository is to install, setup, and configure all of the devices on my network. This is primarily handled with Ansible playbooks with the addition of a handful of terminal scripts and other utilities when ansible
can't make the changes such as post Operating System install but prior to installing Ansible.

## Prerequisites

### Ventoy USB

Ventoy is a operating system install tool that can store several ISO's onto a USB drive that you can then choose to install when you boot from the Ventoy USB.
The idea being that it will be easier in the future to add ISO's to your usb and you don't have to constantly reformat the USB.

Ventoy creates an exFAT or NTFS parition by default and we can save iso files and any other file onto this partition
which will become important as we create and add other configurations and additional operating system installs.
Downloading Ventoy from their [downloads page](https://www.ventoy.net/en/download.html) gives us a tar.gz file that we need to extract.

```bash
tar -xvzf ventoy-1.1.05-linux.tar.gz
```

Which creates a `ventoy-1.1.05-linux` folder in the working directory your terminal is in. I moved this to my home
directory.

```bash
mv ventoy-1.1.05-linux ~/ventoy
```

This also renamed the folder containing everything to just ventoy making the later scripts a bit easier.

Next we need our usb drive. I am using a 256GB drive for this. In order to make sure I have the right device name
I used the `lsblk` command and found my usb device at `/dev/sdc`. Another useful command is `sudo fdisk -l` to list
out all disks and partitions on your device.

Now we can install ventoy onto the `/dev/sdc` usb drive.

```bash
cd ~/ventoy
sudo sh Ventoy2Disk.sh -i /dev/sdc
```

From here, the Ventoy usb should be available to add files onto from your machine. I created a folder for my
Arch and Debian iso's and additional files.

```
Ventoy-USB/
├── ventoy/
│   └── ventoy.json
├── ArchLinux/
│   ├── InstallScripts/
│   │   └── setup.sh
│   ├── archlinux-version-x86_64.iso
│   └── archlinux-version-x86_64.iso.sig
└── Debian/
    ├── InstallScripts/
    │   └── setup.sh
    └── debian-version-amd64-DVD-1.iso
```

## Debian Network Server

---

Some of the containers are development containers as well as a local network App/Dashboard to be accessed by machines on the local network and to host some cool functions including internet of things type controls.

The way this works is through the included Preseed configuration to configure Debian during the install and then an Ansible Configuration file named `setup.yml` that runs post Debian OS configuration.

### Debian Install Overview

Details of the Debian install are covered in this linked [README](./roles/debian_server/README.md).

### Run Debian Install

## Arch Linux Desktop

---

I am making the move to Arch Linux and I will be handling a lot of the installation using the configurations and
scripts found in this repository.

### Arch Install Overview

### Run Arch Install

## Raspberry PI Device

---

### Raspberry Pi Overview

Installing the raspberry pi os onto a raspberry pi can be done using the raspberry pi imager that can be opened from the firmware as long as it is updated or newer on the device. That may require a single sd card that has
that newer firmware available and then installed onto the raspberry pi.

If that firmware is available on the raspberry pi then we can boot the raspberry pi with a blank sd card, boot into the raspberry pi imager on the device, and use a usb stick with the raspberry pi os iso and then install
it onto the raspberry pi device. Then once that is all finished we could run our ansible playbooks for the raspberry pi.

### Run Raspberry Pi Install
