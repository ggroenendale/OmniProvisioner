# Debian Router

I'm interested in a custom Router for my Network. I want to be able to control DHCP and DNS with relative ease
especially as I create web apps that I want to run on my network with their own domain names to make it easier

## Overview of Requirements

### Base OS -> Debian

Debian should be enough to run this device with.

### 10 Gig communcation

I also want something that can communicate with other devices over a 10 gig connection where possible. This will
require a 10 gig NIC (Network Card) using one of the PCIE lanes.

### Internet Access agnostic

It should be able to connect to the internet from another device such as a modem or router that is already
connected to the internet, this router should just bridge the connection.

### VPN

This device should be the VPN device for everything on the network and make it a breeze to have everything
else be secure.

### Wireless access points

Wireless access points will be separate devices connected to this device.

### Hardware requirements

This shouldn't need more than a quad core processor and 16GB of ram. I will probably bump it to 32 GB for future
proofing. I will also use either a 256GB or 500GB hard drive, basically whatever I have laying around or whatever
is cheapest.

### Configuration with Ansible

Incase anything in the device fails I will have my configuration saved in an ansible config in my Git repo making
it easy to reinstall everything.

## Network Notes

### Overview

Just some notes about the network and my plan for it. For starters the IP address plan is ideally based on a 10.0.0.0 subnet if I can control that.

- 10.0.0.1: Router, DNS, DHCP
- 10.0.0.2-9: Unused. Could make separate devices or VM's for DHCP and DNS
- 10.0.0.11-49: Servers, NAS, webservers
- 10.0.0.51-99: Mobile Devices, cell phones, tablets
- 10.0.0.101-199: IOT devices, RaspberryPi, Cameras
- 10.0.0.201-250: Desktop, Laptop, Workstations
