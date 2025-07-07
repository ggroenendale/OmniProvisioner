"""Installation of Arch Linux using python to configure settings"""

import subprocess
from pathlib import Path
import glob

from archinstall.lib.installer import Installer
from archinstall.lib.general import SysCommand
from archinstall.default_profiles.minimal import MinimalProfile
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
ARCH_HOSTNAME = "arch_desktop"
ARCH_USERNAME = "install_wizard"
with open("password_user.txt", "r", encoding="utf-8") as pass_file:
    ARCH_PASSWORD = pass_file.read()

with open("password_encr.txt", "r", encoding="utf-8") as encr_file:
    ENCR_PASSWORD = encr_file.read()

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

device_path = Path("/dev/nvme0n1")

# get the physical disk device
device = device_handler.get_device(device_path)
print(device)
if not device:
    RuntimeError("Couldnt parse device")

# Create a device modification object
device_modification = DeviceModification(device, wipe=True)

# create a new boot partition
boot_partition = PartitionModification(
    status=ModificationStatus.Create,
    type=PartitionType.Primary,
    start=Size(1, Unit.MiB, device.device_info.sector_size),
    length=Size(2, Unit.GiB, device.device_info.sector_size),
    mountpoint=Path("/efi"),
    fs_type=FilesystemType.Fat32,
    flags=[PartitionFlag.ESP],
)
device_modification.add_partition(boot_partition)

swap_partition = PartitionModification(
    status=ModificationStatus.Create,
    type=PartitionType.Primary,
    start=Size(1, Unit.MiB, device.device_info.sector_size) + boot_partition.length,
    length=Size(70, Unit.GiB, device.device_info.sector_size),
    mountpoint=None,
    fs_type=FilesystemType.LinuxSwap,
    mount_options=[],
    flags=[PartitionFlag.SWAP],
)
device_modification.add_partition(swap_partition)

# create a root partition

root_length = (
    device.device_info.total_size
    - boot_partition.length
    - swap_partition.length
    - Size(100, Unit.MiB, device.device_info.sector_size)
)

root_partition = PartitionModification(
    status=ModificationStatus.Create,
    type=PartitionType.Primary,
    start=Size(1, Unit.MiB, device.device_info.sector_size)
    + boot_partition.length
    + swap_partition.length,
    length=root_length,
    mountpoint=None,
    fs_type=FilesystemType.Btrfs,
    mount_options=[],
    btrfs_subvols=[
        SubvolumeModification(name="@", mountpoint=Path("/")),
        SubvolumeModification(name="@boot", mountpoint=Path("/boot")),
        SubvolumeModification(name="@home", mountpoint=Path("/home")),
        SubvolumeModification(name="@snapshots", mountpoint=Path(".snapshots")),
        SubvolumeModification(name="@var", mountpoint=Path("/var")),
        SubvolumeModification(name="@log", mountpoint=Path("/var/log")),
        SubvolumeModification(name="@cache", mountpoint=Path("/var/cache")),
        SubvolumeModification(name="@tmp", mountpoint=Path("/var/tmp")),
        SubvolumeModification(name="@opt", mountpoint=Path("/opt")),
        SubvolumeModification(name="@docker", mountpoint=Path("/var/lib/docker")),
        SubvolumeModification(
            name="@games", mountpoint=Path(f"/home/{ARCH_USERNAME}/Games")
        ),
        SubvolumeModification(name="@pkg", mountpoint=Path("/var/cache/pacman/pkg")),
    ],
)
device_modification.add_partition(root_partition)

# Define the Disk Configuration here using the combined modifications
disk_config = DiskLayoutConfiguration(
    config_type=DiskLayoutType.Default,
    device_modifications=[device_modification],
)

# Disk encryption configuration
# disk_encryption = DiskEncryption(
#    encryption_password=Password(plaintext=ENCR_PASSWORD),
#    encryption_type=EncryptionType.Luks,
#    partitions=[root_partition],
#    hsm_device=None,
# )

# disk_config.disk_encryption = disk_encryption

"""
============================================================================================================================
    Begin the Actual Installation
============================================================================================================================
"""

# Initiate file handler with the disk config and the optional disk encryption config
fs_handler = FilesystemHandler(disk_config=disk_config)

# Perform all file operations
# WARNING: this will potentially format the filesystem and delete all data
fs_handler.perform_filesystem_operations(show_countdown=False)


# Start the guided installation
with Installer(
    target=Path("/mnt"),
    disk_config=disk_config,
    base_packages=[
        "base",
        "base-devel",
        "linux-firmware",
        "linux",
        "linux-lts",
        "linux-zen",
        "linux-hardened",
        "grub",
        "efibootmgr",
    ],
    kernels=["linux"],
) as installation:
    installation.mount_ordered_layout()

    # Set the hostname for the machine and the locale
    installation.minimal_installation(
        hostname=ARCH_HOSTNAME,
        locale_config=LocaleConfiguration(
            kb_layout="us", sys_lang="en_US", sys_enc="UTF-8"
        ),
    )

    # Add grub as bootloader
    #installation.add_bootloader(Bootloader.Grub)

    SysCommand(f"arch-chroot {installation.target} /bin/bash -c " + '"echo ' + "'GRUB_ENABLE_CRYPTODISK=y'" + ' >> /etc/default/grub"')

    command = [
        'arch-chroot',
        installation.target,
        'grub-install',
        '--debug',
        '--target=x86_64-efi',
        '--efi-directory=/efi',
        '--boot-directory=/boot',
        '--bootloader-id=GRUB',
        '--removable'
    ]
    
    SysCommand(command, peek_output=True)

    SysCommand(f"arch-chroot {installation.target} grub-mkconfig -o /boot/grub/grub.cfg")

    # Make a minimup profile to install the network config to
    profile_config = ProfileConfiguration(MinimalProfile())
    profile_handler.install_profile_config(installation, profile_config)

    # Define the network setup which should pull from the config file
    network_config: NetworkConfiguration = NetworkConfiguration(
        type=NicType.MANUAL,
        nics=[
            Nic(
                iface="eno1",
                ip="192.168.1.101",
                dhcp=True,
                gateway="192.168.1.1",
                dns=["9.9.9.9", "1.1.1.1"],
            )
        ],
    )

    if network_config:
        network_config.install_network_config(installation, profile_config)

    mirror_config = MirrorConfiguration(
        mirror_regions=[
            MirrorRegion(
                name="Worldwide",
                urls=[
                    "https://geo.mirror.pkgbuild.com/$repo/os/$arch",
                    "https://ftpmirror.infania.net/mirror/archlinux/$repo/os/$arch",
                ],
            ),
            MirrorRegion(
                name="Sweden",
                urls=[
                    "https://mirror.osbeck.com/archlinux/$repo/os/$arch",
                    "https://mirror.accum.se/mirror/archlinux/$repo/os/$arch",
                ],
            ),
            MirrorRegion(
                name="Germany",
                urls=[
                    "https://de.arch.niranjan.co/$repo/os/$arch",
                    "https://archlinux.thaller.ws/$repo/os/$arch",
                ],
            ),
            MirrorRegion(
                name="France",
                urls=[
                    "https://mirror.cyberbits.eu/archlinux/$repo/os/$arch",
                    "https://fr.mirrors.cicku.me/archlinux/$repo/os/$arch",
                ],
            ),
            MirrorRegion(
                name="Canada",
                urls=[
                    "https://mirror.franscorack.com/archlinux/$repo/os/$arch",
                    "https://ca.mirrors.cicku.me/archlinux/$repo/os/$arch",
                ],
            ),
            MirrorRegion(
                name="Finland",
                urls=[
                    "http://cdnmirror.com/archlinux/$repo/os/$arch",
                    "https://fi.arch.niranjan.co/$repo/os/$arch",
                ],
            ),
            MirrorRegion(
                name="Switzerland",
                urls=[
                    "https://theswissbay.ch/archlinux/$repo/os/$arch",
                    "https://ch.mirrors.cicku.me/archlinux/$repo/os/$arch",
                ],
            ),
            MirrorRegion(
                name="Norway", urls=["https://mirror.neuf.no/archlinux/$repo/os/$arch"]
            ),
            MirrorRegion(
                name="Netherlands",
                urls=[
                    "https://nl.arch.niranjan.co/$repo/os/$arch",
                    "https://nl.mirrors.cicku.me/archlinux/$repo/os/$arch",
                ],
            ),
            MirrorRegion(
                name="Estonia",
                urls=[
                    "https://mirror.cspacehostings.com/archlinux/$repo/os/$arch",
                    "https://repo.br.ee/arch/$repo/os/$arch",
                ],
            ),
            MirrorRegion(
                name="Japan",
                urls=[
                    "https://jp.mirrors.cicku.me/archlinux/$repo/os/$arch",
                    "https://repo.jing.rocks/archlinux/$repo/os/$arch",
                ],
            ),
            MirrorRegion(
                name="Singapore",
                urls=[
                    "https://singapore.mirror.pkgbuild.com/$repo/os/$arch",
                    "https://mirror.freedif.org/archlinux/$repo/os/$arch",
                ],
            ),
            MirrorRegion(
                name="Australia",
                urls=[
                    "https://au.arch.niranjan.co/$repo/os/$arch",
                    "https://gsl-syd.mm.fcix.net/archlinux/$repo/os/$arch",
                ],
            ),
        ]
    )
    
    
    print("Setting up Mirrors...")
    installation.set_mirrors(mirror_config=mirror_config)

    installation.add_additional_packages(["nano", "ansible", "git", "wget"])

    installation.set_timezone(zone="America/Vancouver")
