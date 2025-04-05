#!/bin/bash

# First make sure the 3.0.2 version of the archinstall library is cloned to the device
#curl https://github.com/archlinux/archinstall/archive/refs/tags/3.0.2.zip -o /tmp/archinstall.zip
#unzip /tmp/archinstall.zip

# Make sure to install archinstall in the working directory
#cd archinstall
#pip install .

# cd up a folder to return to the working directory
#cd ..

# Then run archinstall using the install_arch.py configuration file
python install_arch.py

# Finally run the ansible playbook to do the bulk of the configuration.
sudo ansible-playbook OmniProvisioner/playbooks/desktop.yaml
