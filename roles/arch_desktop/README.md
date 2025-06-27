# Arch Linux install and Setup

I am making the move to Arch Linux and I will be handling a lot of the installation using the configurations and
scripts found in this repository.

## Installation

---

### Quickstart Install

1. Boot into the Arch Linux live environment
2. Mount the Ventoy USB
3. Run the `copy_files_to_newiso.sh` script
4. Run the `arch_install.sh`

### Reasons for using Archinstall

For starters I am moving away from Ubuntu to Arch Linux. I started to experiment with Neovim and found hyprland
also interesting and I have wanted to create a custom setup for a long while now. I think I will find comfort in
being able to install the packages piece by piece and understanding a bit more of the underlying pieces and
hopefully that will lead to a faster system. I have also found some things I didn't like with Ubuntu like the
move to Snap. I am sure there are a litany of other solutions I could go with including staying with Ubuntu and
using Neovim there and I could probably setup hyprland as well. Or I could move to one of the "almost Arch"
distros. But ultimately the amount of time spent researching and discovery into finding the right distro could
instead be spent going with Arch where I could research the individual packages I want and creating my forever
Operating System.

This move to Arch also coincides with moving my home network server from Ubuntu to Debian.

I chose to handle the installation this way rather than going the manual route and reading the wiki to make sure
this process is repeatable and editable as I learn how to use Arch and Install it. The whole idea of a "Forever
Operating System" being that I will continually modify my configuration and the applications I use, and get really
comfortable with wiping and reinstalling Arch.

I know that for myself in the event that the installation doesn't work or I don't like something I will give up
and move to a different Linux distro.

### Process

---

Our end goal is to manage most of the Arch configuration with an Ansible playbook. In order to run an ansible
playbook we first need to install Ansible and also have some of the basic configurations like the file system and
partitions.

We will begin with the `archiso` package so we can modify a fresh Arch ISO. We are going to add a script that runs
a basic archinstall config to make sure the hard drive is partitioned, mirrors are configured, and install ansible.

We can run `archiso` while in an Arch live environment and we can modify that iso or download and configure a newer
iso. From within the iso, we can copy the `releng` archiso configuration to the home folder of the root user
in the live environment. We can then edit the files inside this iso copy and place an `install.sh` bash script
to run upon os install.

This is the script that will first run archinstall, and then run ansible.

In order for the archinstall to run correctly, we need to install our python and json configuration files into the
iso copy. The last thing the archinstall config should do is clone this repository in order to get the latest
configs and then run the playbook.

### Installation

---

#### Archiso install

To begin with we need to be working within an Arch iso live environment. So we will boot into the Arch linux live
environment from our Ventoy USB. We then need to make sure the archiso package is installed. A fresh arch iso
should include this package, however we can also install it with pacman:

```bash
sudo pacman -S archiso
```

We are going to create an iso that on install runs the archinstall module with our python file configuration. We
can copy the `releng` configuration from the `archiso` directory into a working folder to edit it.

```bash
cp -r /usr/share/archiso/configs/releng ~/new-iso
```

#### Python 3.13

The Arch Linux ISO version that I am currently working with is `2025.03.01` and this comes with Python 3.13.2 so
this should work out of the box for our script.

However if we need to fix the installation, and we are inside the barebones iso we can install Python to the iso
and rebuild it.

```bash
pacman -Sy python
```

#### Archinstall

The version of the archinstall library that is in the March 1st 2025 iso is 3.0.2 thus our python and json files
need to conform with this version.

To use archinstall we just need to run our python file, we dont need to run archinstall as a python module.

```bash
python install_arch.py
```

#### Ansible

To run our ansible configuration, after the archinstall configuration installs ansible, we can run our ansible
playbook with the `ansible-playbook` command with our desktop playbook:

```bash
ansible-playbook playbooks/desktop.yaml
```

#### Copy files into new arch iso

After adding our files to the new iso configuration the folder structure should look like this:

```
new-iso/
├── airootfs/
│   ├── etc/
│   ├── root/
│   │   ├── OmniProvisioner/   # These files will be cloned during the archinstall script
│   │   │   ├── group_vars/
│   │   │   ├── playbooks/
│   │   │   ├── requirements/
│   │   │   ├── roles/
│   │   │   └── ansible.cfg
│   │   ├── arch_install.sh    # install script
│   │   ├── install_arch.py    # archinstall configuration
│   │   ├── archconfig.json    # json configuration
│   │   └── .vault_pass.txt    # Secrets password file, moved into OmniProvisioner by archinstall
│   └── usr/
├── efiboot/
├── grub/
├── syslinux/
├── bootstrap_packages.x86_64
├── packages.x86_64
├── pacman.conf
└── profiledef.sh
```

To do this run the `copy_files_to_newiso.sh` bash script.

#### Build the new iso

Once that is taken care of, run `mkarchiso` to build the new iso, and save this iso back to the Ventoy USB.

```bash
mkarchiso -v -w /tmp/archiso-work -o /tmp /mnt/newiso
```

#### Boot into the new iso and run arch_install.sh

At this point the base configuration should be all setup in our new iso, and we have booted into that iso. It
should be as simple as running the install script and then rebooting.

```bash
arch_install.sh
```

## Development

### Archinstall configuration

In order to develop the archinstall config with the correct version in our arch iso which is 3.0.2, we can copy
the release file from github, unpack and install the library into a development virtual environment.

```bash
curl https://github.com/archlinux/archinstall/archive/refs/tags/3.0.2.zip -o /tmp/archinstall.zip
unzip /tmp/archinstall.zip
```

This will download the 3.0.2 version into the `/tmp` directory and then unzip it into the working directory as the
folder `archinstall`

We then need to navigate into the new archinstall folder and pip install its contents

```bash
cd archinstall
pip install .
```

## Overview of Whats Included

---

The software, packages, and tools to be installed in this configuration are broken down into these categories:

- System Packages and Utilities
- System Monitoring and Debugging
- User and Security Management
- File System and Disk Tools
- Networking and DNS
- Desktop Environment
- Development and CLI Tools
- Additional Software

> NOTE: In order to see a list of packages and their versions that come with the iso we are working with we can
> navigate to the following url: [https://archive.archlinux.org/iso/2025.03.01/arch/pkglist.x86_64.txt](https://archive.archlinux.org/iso/2025.03.01/arch/pkglist.x86_64.txt)
> take note of the date which is the version of the arch linux iso, at the time of writing we are working with the
> March 01, 2025 build.

### System Tools and Utilities

#### SSH

#### Nvidia Drivers

#### GRUB

#### Paru

#### Fonts

### System Monitoring and Debugging

### User and Security Management

### File System and Disk Tools

#### btrfs-progs

#### Parted

#### rsync

#### zstd

### Networking and DNS

#### Networkmanager

#### wget & curl

### Desktop Environment -> Custom

I may come to regret this decision but I have decided to essentially combine all of the things I would normally
get with a desktop environment and just put in place each one that I want. I think I have a problem with
installing a monolithic piece of software with a bunch of dependencies that may become hard to manage as time
goes on. I think this will also give me more flexibility as I go through the process of setting up Arch the way
I want it.

I especially like the idea of updating 1 part of my configuration and not having the entire component of software
fail. However, I can picture some issues arising if two components rely on one library and one of those components
needs a different version of that library. If for example Waybar and Hyprland each need a different version of
Python and installing the newer version and removing the older version somehow breaks one of those components.

But we will cross that bridge when or if we get to it.

#### Sound -> Pipewire

#### Terminal -> Wezterm

Wezterm is my preferred terminal. I like that it is customizable in lua which is just a delightful easy language.

#### Window Manager -> Hyprland

Hyprland is the goat and I am excited to get into customizing it.

#### App Launcher -> Fuzzel or Walker

I decided to go with fuzzel. It's wayland native which should jive well with Hyprland which also depends on
Wayland. It can also be customized using a fuzzel.ini file in `.config/fuzzel`. I've also been looking at Walker
which seems to have more recent development and might be less resource intensive. I am not sure yet.

#### Authentication Agent -> hyprpolkitagent

The thing that pops up when you need to authenticate something.

#### File Manager -> Thunar

I'm not real sure on File Managers. I know that I'm not super satisfied with Nautilus and Dolphin seems like its
a bit too heavy for what I need. Thunar also seems pretty extensible so I think for now we will go with that.

#### Panels, System Tray, & Widgets -> Waybar & Eww

Waybar is also Wayland based and works with Hyprland and Fuzzel. I'm also including Eww as well for custom
widgets.

#### Notifications -> Mako

Seen this recommended a couple times for notifications.

#### Settings & System Configuration -> Several

I first want to note `xdg-desktop-portal-hyprland` and I will explain more about what it does another time

#### Wallpaper -> swww

It seems to have the most customization and I think it supports animated wallpapers. Also seems to make it easy
to switch wallpapers or write a script that changes them.

#### Clipboard -> clipman + wl-clip-persist

I am still unsure between clipman and cliphist which one is best, because cliphist is able to copy images to the
clipboard but with clipman I at least found a simple config to tie it with fuzzel. wl-clip-persist extends the
history for the clipboard to include stuff even if an application closes.

### Development tools

#### Git + Credential Manager

#### Neovim

#### k3s

#### kdash

### Additional Software

#### Browser -> LibreWolf + Zen Browser

This decision was more in the realm of what is performant and privacy focused but also helps me as a web app
developer. So far I am looking at Librewolf for the privacy focus and I also like Thorium. I may also install Zen
browser depending on if I want something that is quiet and nice to use.

After some testing I found LibreWolf to be faster than Thorium on Ubuntu 22.04. I found Thorium to be a bit
buggy with some graphical errors. It may be some configuration issues or some miscommunication with Nvidia.
But for simplicity I am going to stick with LibreWolf.

I also tested Zen browser and I really like it. I could see using Zen browser as a replacement for installing
the Spotify Linux app or other desktop apps.

### Other Packages

This will mostly serve as a space for me to remember all of the tools that I use and dump some things from my brain.

A list of packages I need to install that are particularly necessary as libraries or installers

- cargo
- nvm
- npm
- nodejs
- helm
- gem
- ruby-full
- stow
- fd-find
- ripgrep
- luarocks
- libparted-dev
- Spark
- Zot (OCI Container registry)
- Podman
- gawk (makes bash config editing scripts work)

### Notes from python config file

Node js install:
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash

in lieu of restarting the shell
\. "$HOME/.nvm/nvm.sh"

nvm install 22

node -v # Should print "v22.14.0".

nvm current # Should print "v22.14.0".

npm -v # Should print "10.9.2".

apt install wezterm
apt install stow
curl https://raw.githubusercontent.com/jesseduffield/lazydocker/master/scripts/install_update_linux.sh | bash
Commandline: apt install gem
Commandline: apt install ruby-full
Commandline: apt install -y nodejs
Commandline: apt install stow
Commandline: apt install fd-find
Commandline: apt install pip
Commandline: apt install xclip xsel wl-clipboard
Commandline: apt-get install ripgrep
Commandline: apt install luarocks
Commandline: apt install libparted-dev

Commandline: apt install python3.12 python3.12-venv
Commandline: apt install python3.12-dev
geoff@geoff-ubuntu:~$
