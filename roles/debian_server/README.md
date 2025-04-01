# Debian Network Server install

---

## Introduction

---

The purpose of this repository is to setup my new Debian network server. This server is both a file storage server and a machine to host Kubernetes containers and a Postgres Database.

Some of the containers are development containers as well as a local network App/Dashboard to be accessed by machines on the local network and to host some cool functions including internet of things type controls.

The way this works is through the included Preseed configuration to configure Debian during the install and then an Ansible Configuration file named `setup.yml` that runs post Debian OS configuration.

## Overview

### Services and Packages

This will serve as the growing list of services and packages that I want running on this server.

- k3s
- Spark
- Postgres
- File storage...
- Zot (Local Container Registry)
- Podman

## Installation

---

Here is the step by step:

### 3) Setup Ansible and other scripts on USB stick

Ventoy creates a standard FAT32/ExFAT parition, we can add a folder for Ansible and our post-install scripts.

Create ansible folder on USB stick

```bash
mkdir /mnt/ventoy/debian_install
```

Copy the `preseed.cfg`, `postinstall.service`, `setup.sh`, and `playbook.yml` files to the debian_install folder.

```bash
cp preseed.cfg /mnt/ventoy/debian_install
cp postinstall.service /mnt/ventoy/debian_install
cp setup.sh /mnt/ventoy/debian_install
cp playbook.yml /mnt/ventoy/debian_install
```

### Using Preseed with a USB Stick (Ventoy)

Create a preseed.cfg file and place it on your USB stick.

Boot the Debian ISO with Ventoy.

In the boot menu, press Tab on the installer entry and add:

```
auto url=file:///cdrom/preseed.cfg
```

Press Enter to start the unattended installation.
