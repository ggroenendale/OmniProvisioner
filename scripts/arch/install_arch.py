"""Installation of Arch Linux using python to configure settings"""

import subprocess
from pathlib import Path
import json
import glob

from archinstall.lib.installer import Installer
from archinstall.default_profiles.minimal import MinimalProfile
from archinstall.lib.args import ArchConfig
from archinstall.lib.models import Bootloader
from archinstall.lib.models.device_model import (
    DeviceModification,
    DiskEncryption,
    DiskLayoutConfiguration,
    DiskLayoutType,
    EncryptionType,
    FilesystemType,
    PartitionModification,
    PartitionType,
    PartitionFlag,
    Password,
    ModificationStatus,
    Size,
    Unit,
    SubvolumeModification,
)
from archinstall.lib.disk.device_handler import device_handler
from archinstall.lib.models.network_configuration import (
    NetworkConfiguration,
    Nic,
    NicType,
)
from archinstall.lib.models.profile_model import ProfileConfiguration
from archinstall.lib.models.locale import LocaleConfiguration
from archinstall.lib.models.mirrors import MirrorConfiguration, MirrorRegion
from archinstall.lib.profile.profiles_handler import profile_handler
from archinstall.lib.disk.filesystem import FilesystemHandler

"""
============================================================================================================================
    Required Configuration Variables
============================================================================================================================
"""

ARCHCONFIG_PATH = Path("archconfig.json")
ARCH_HOSTNAME = ""
ARCH_USERNAME = "geoff"
ARCH_PASSWORD = ""
ENCR_PASSWORD = ""

"""
============================================================================================================================
    Installation Functions
============================================================================================================================
"""


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
    Partition Table Definitions
============================================================================================================================
"""

# Find the first NVMe drive in /dev/disk/by-id
nvme_devices = glob.glob("/dev/disk/by-id/nvme*")

if not nvme_devices:
    raise RuntimeError("No NVMe drives found in /dev/disk/by-id/")
if len(nvme_devices) > 1:
    print("Warning: multiple NVMe drives found, using the first.")

selected_nvme = nvme_devices[0]

device_path = Path(selected_nvme)

# get the physical disk device
device = device_handler.get_device(device_path)

# Create a device modification object
device_modification = DeviceModification(device, wipe=True)

# create a new boot partition
boot_partition = PartitionModification(
    status=ModificationStatus.Create,
    type=PartitionType.Primary,
    length=Size(2, Unit.GiB, device.device_info.sector_size),
    mountpoint=Path("/efi"),
    fs_type=FilesystemType.Fat32,
    flags=[PartitionFlag.ESP],
)
device_modification.add_partition(boot_partition)

swap_partition = PartitionModification(
    status=ModificationStatus.Create,
    type=PartitionType.Primary,
    length=Size(70, Unit.GiB, device.device_infog.sector_size),
    mountpoint=None,
    fs_type=FilesystemType.LinuxSwap,
    mount_options=[],
    flags=[PartitionFlag.SWAP],
)
device_modification.add_partition(swap_partition)

# create a root partition

root_length = (
    device.device_info.total_size - boot_partition.length - swap_partition.length
)

root_partition = PartitionModification(
    status=ModificationStatus.Create,
    type=PartitionType.Primary,
    length=root_length,
    mountpoint=None,
    fs_type=FilesystemType.Btrfs,
    mount_options=[],
    btrfs_subvols=[
        SubvolumeModification(name="@", mountpoint="/"),
        SubvolumeModification(name="@boot", mountpoint="/boot"),
        SubvolumeModification(name="@home", mountpoint="/home"),
        SubvolumeModification(name="@snapshots", mountpoint=".snapshots"),
        SubvolumeModification(name="@var", mountpoint="/var"),
        SubvolumeModification(name="@log", mountpoint="/var/log"),
        SubvolumeModification(name="@cache", mountpoint="/var/cache"),
        SubvolumeModification(name="@tmp", mountpoint="/var/tmp"),
        SubvolumeModification(name="@opt", mountpoint="/opt"),
        SubvolumeModification(name="@docker", mountpoint="/var/lib/docker"),
        SubvolumeModification(name="@games", mountpoint=f"/home/{ARCH_USERNAME}/Games"),
        SubvolumeModification(name="@pkg", mountpoint="/var/cache/pacman/pkg"),
    ],
)
device_modification.add_partition(root_partition)

# Define the Disk Configuration here using the combined modifications
disk_config = DiskLayoutConfiguration(
    config_type=DiskLayoutType.Default,
    device_modifications=[device_modification],
)

# Disk encryption configuration
disk_encryption = DiskEncryption(
    encryption_password=Password(plaintext=ARCH_PASSWORD),
    encryption_type=EncryptionType.Luks,
    partitions=[root_partition],
    hsm_device=None,
)

disk_config.disk_encryption = disk_encryption

# Initiate file handler with the disk config and the optional disk encryption config
fs_handler = FilesystemHandler(DISK_CONFIG, DISK_ENC)

# Perform all file operations
# WARNING: this will potentially format the filesystem and delete all data
fs_handler.perform_filesystem_operations()


# Start the guided installation
with Installer(
    target=MOUNTPOINT, disk_config=DISK_CONFIG, kernels=KERNELS
) as installation:
    installation.mount_ordered_layout()

    if installation.minimal_installation():
        # Set the hostname for the machine from the config file
        installation.set_hostname(hostname=config.hostname)

        # Add grub as bootloader
        installation.add_bootloader(Bootloader.Grub)

        # Define the network setup which should pull from the config file
        network_config: NetworkConfiguration | None = config.network_config

        if network_config:
            network_config.install_network_config(installation, config.profile_config)

        profile_config = ProfileConfiguration(MinimalProfile())
        profile_handler.install_profile_config(installation, profile_config)

    installation.add_additional_packages(config.packages)
