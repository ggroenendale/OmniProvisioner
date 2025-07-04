# Omni Provisioner

Omni as in all devices

Provisioner as in this repository will be used to provision and configure all of my devices.

<!-- mtoc-start -->

* [Introduction](#introduction)
* [Prerequisites](#prerequisites)
  * [Ventoy USB](#ventoy-usb)
    * [Encrypt USB](#encrypt-usb)
    * [Install Ventoy](#install-ventoy)
* [Debian Network Server](#debian-network-server)
  * [Debian Install Overview](#debian-install-overview)
  * [Run Debian Install](#run-debian-install)
* [Arch Linux Desktop](#arch-linux-desktop)
  * [Arch Install Overview](#arch-install-overview)
  * [Run Arch Install](#run-arch-install)
* [Raspberry PI Device](#raspberry-pi-device)
  * [Raspberry Pi Overview](#raspberry-pi-overview)
  * [Run Raspberry Pi Install](#run-raspberry-pi-install)
* [Mobile Device](#mobile-device)
  * [Mobile Device Overview](#mobile-device-overview)

<!-- mtoc-end -->

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
├── isos/
│   ├── Arch
│   ├── Debian
│   └── RaspberryPi
├── playbooks/
│   ├── desktop.yaml
│   ├── device.yaml
│   └── server.yaml
├── requirements/
│   └── common.yaml
├── roles/
│   ├── arch_desktop/
│   │   └── tasks
│   ├── debian_server/
│   │   └── tasks
│   └── raspberrypi_device/
│       └── tasks
├── scripts/
│   ├── arch/
│   │   └── arch_install.sh
│   ├── debian/
│   │   └── debian_install.sh
│   └── raspberrypi/
│       └── raspberrypi_install.sh
├── .gitignore
├── ansible.cfg
└── README.md
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

Details of the Arch install are covered in this linked [README](./roles/arch_desktop/README.md)

### Run Arch Install

## Raspberry PI Device

---

### Raspberry Pi Overview

Installing the raspberry pi os onto a raspberry pi can be done using the raspberry pi imager that can be opened from the firmware as long as it is updated or newer on the device. That may require a single sd card that has
that newer firmware available and then installed onto the raspberry pi.

If that firmware is available on the raspberry pi then we can boot the raspberry pi with a blank sd card, boot into the raspberry pi imager on the device, and use a usb stick with the raspberry pi os iso and then install
it onto the raspberry pi device. Then once that is all finished we could run our ansible playbooks for the raspberry pi.

### Run Raspberry Pi Install

## Mobile Device

---

### Mobile Device Overview

I am also in the process of looking for a future mobile device solution that I can rely on. Mostly what I want is a way to keep the phone clean of bloatware and create my own apps and make it work with my other systems
somewhat seemlessly.

It seems the primary way to make this work is to not use Verizon for the phone. It seems like Mint Mobile or something similar is my best pathway forward. I could also get a data sim card for a future tablet or laptop
that I use remotely, even my HP Elitebook has a sim card slot and a WWAN card.

The options that are dividing me the most are:

- Device Memory: I want at least 8GB of RAM possibly more
- Customizable: I want to be able to write applications ideally in Python, I might slug it out and learn Java or Kotlin to make other things if I have to get an Android device.
- Degoogled, private, secure: hence the open source software and as much access and permissions as possible
- Repairable: This means if parts go bad I want to be able to replace them, also be able to reinstall the software via ansible
- 2 sim cards?: This is a low priority but its nice to have. It might be mostly important that its an actual card and not just eSIM

Phone features that I actually need regardless of solution:

- Bluetooth: I need this for headphones and music and calls
- Decent battery life: not a big concern as long as it doesnt limit me
- USB-C Charging: Non-negotiable
- MicroSD storage: Non-negotiable
- Camera: The actual camera quality doesn't matter much, but whatever OS I choose needs to be able to use the camera
- GPS: Non-negotiable, I need maps
- NFC: not absolutely critical but would be nice to have, I'm not even sure I could use this for payments with open source software
