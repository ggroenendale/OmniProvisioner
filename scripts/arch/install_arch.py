"""Installation of Arch Linux using python to configure settings


"""
import subprocess
from pathlib import Path
import json
import glob

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

"""
============================================================================================================================
    Required Configuration Variables
============================================================================================================================
"""

ARCHCONFIG_PATH = Path("archconfig.json")
ARCH_USERNAME = "geoff"

"""
============================================================================================================================
    Installation Functions
============================================================================================================================
"""


def load_arch_config(username: str) -> ArchConfig:
    """
    This function injects the correct NVME drive id
    into the json configuration file before loading it and returning
    it for the rest of the installation.

    :param username: The username to write into the JSON where necessary.
    :type username: str
    """
    # Find the first NVMe drive in /dev/disk/by-id
    nvme_devices = glob.glob("/dev/disk/by-id/nvme*")

    if not nvme_devices:
        raise RuntimeError("No NVMe drives found in /dev/disk/by-id/")
    if len(nvme_devices) > 1:
        print("Warning: multiple NVMe drives found, using the first.")

    selected_nvme = nvme_devices[0]

    # Load the existing Archinstall config
    with open(ARCHCONFIG_PATH, "r", encoding="utf8") as f:
        json_config = json.load(f)

    # Inject the NVMe ID into disk_config
    for mod in json_config.get("disk_config", {}).get("device_modifications", []):
        mod["device"] = selected_nvme

    # Update the Games mountpoint with the correct username
    btrfs_subvolumes = json_config["disk_config"]["device_modifications"][2]["btrfs"]

    btrfs_subvolumes.append({
        "name": "@games",
        "mountpoint": f"/home/{username}/Games",
        "mount_options": [
            "noatime",
            "ssd",
            "space_cache=v2",
            "discard=async"
        ]
    })

    # Save the updated config (or return it if you want to pass directly)
    with open(ARCHCONFIG_PATH, "w", encoding="utf8") as f:
        json.dump(json_config, f, indent=2)

    print(f"✔ Replaced device path with: {selected_nvme}")

    # Unclear if this old line actually loads my jsonconfig
    # return arch_config_handler.config
    return ArchConfig.model_validate_json(json.dumps(json_config))


def run_command(command, check=True):
    """
    Helper function to run shell commands

    :param command: The terminal command as a string.
    :type command: str
    :param check: Passes to subprocess.run(...,...,check=check)
    :type check: bool
    """
    subprocess.run(command, shell=True, check=check)


"""
============================================================================================================================
    Begin the Actual Installation
============================================================================================================================
"""

# ArchConfig builder from json config
config: ArchConfig = load_arch_config(username=ARCH_USERNAME)

# Not sure if the mountpoint here is necessary if its available in the config
MOUNTPOINT = "/mnt"
DISK_CONFIG: DiskLayoutConfiguration = config.disk_config

data_store = {}
DISK_ENC = DiskEncryptionMenu(DISK_CONFIG.device_modifications, data_store).run()
KERNELS = ["linux"]

# Initiate file handler with the disk config and the optional disk encryption config
fs_handler = FilesystemHandler(DISK_CONFIG, DISK_ENC)

# Perform all file operations
# WARNING: this will potentially format the filesystem and delete all data
fs_handler.perform_filesystem_operations()


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

