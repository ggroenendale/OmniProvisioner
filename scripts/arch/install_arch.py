"""Installation of Arch Linux using python to configure settings


"""
import subprocess
import pathlib
import json

from archinstall.lib.installer import Installer
from archinstall.default_profiles.minimal import MinimalProfile
from archinstall.lib.args import ArchConfig, arch_config_handler
# from archinstall.lib.configuration import ConfigurationOutput
from archinstall.lib.models import User, Bootloader
from archinstall.lib.models.device_model import DiskLayoutConfiguration
from archinstall.lib.models.network_configuration import NetworkConfiguration
from archinstall.lib.models.profile_model import ProfileConfiguration
from archinstall.lib.interactions.disk_conf import select_disk_config
from archinstall.lib.disk.encryption_menu import DiskEncryptionMenu
from archinstall.lib.disk.filesystem import FilesystemHandler
from archinstall.lib.profile import profile_handler

# ArchConfig builder from json config
config: ArchConfig = arch_config_handler.config

# Not sure if the mountpoint here is necessary if its available in the config
MOUNTPOINT = "/mnt"
DISK_CONFIG: DiskLayoutConfiguration = select_disk_config()

data_store = {}
DISK_ENC = DiskEncryptionMenu(DISK_CONFIG.device_modifications, data_store).run()
KERNELS = ["linux"]

# initiate file handler with the disk config and the optional disk encryption config
fs_handler = FilesystemHandler(DISK_CONFIG, DISK_ENC)

# Perform all file operations
# WARNING: this will potentially format the filesystem and delete all data
fs_handler.perform_filesystem_operations()


def run_command(command, check=True):
    """
    Helper function to run shell commands

    :param command: The terminal command as a string.
    :type command: str
    :param check: Passes to subprocess.run(...,...,check=check)
    :type check: bool
    """
    subprocess.run(command, shell=True, check=check)


def setup_provisioner_files(username):
    """
    Clones ansible files into the root working directory 

    """
    # Git repository containing ansible configs
    ansible_repo = "https://github.com/ggroenendale/OmniProvisioner.git"

    # Clone the ansible repo
    run_command(f"git clone {ansible_repo}")
    # Move the vault password file into the ansible repository
    run_command(f"mv .vault_pass.txt OmniProvisioner/")


# Start the guided installation
with Installer(
        target=MOUNTPOINT,
        disk_config=DISK_CONFIG,
        disk_encryption=DISK_ENC,
        kernels=KERNELS) as installation:
    installation.mount_ordered_layout()

    if installation.minimal_installation():
        # Set the hostname for the machine from the config file
        installation.set_hostname(hostname=config.hostname)

        # Add grub as bootloader
        installation.add_bootloader(Bootloader.Grub)

        # Define the network setup which should pull from the config file
        network_config: NetworkConfiguration | None = config.network_config

        if network_config:
            network_config.install_network_config(
                installation,
                config.profile_config
            )

        profile_config = ProfileConfiguration(MinimalProfile())
        profile_handler.install_profile_config(installation, profile_config)

        # Clone OmniProvisioner
        setup_provisioner_files()
