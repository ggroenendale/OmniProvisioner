# Copy the vault pass text file to Ventoy
cp -r .vault_pass.txt /media/geoff/Ventoy/

# Copy Arch Linux scripts to Ventoy
cp -r scripts/arch/arch_install.sh /media/geoff/Ventoy/scripts/arch/arch_install.sh
cp -r scripts/arch/archinstall-configure-newiso.sh /media/geoff/Ventoy/scripts/arch/archinstall-configure-newiso.sh
cp -r scripts/arch/install_arch.py /media/geoff/Ventoy/scripts/arch/install_arch.py

# Copy Debian scripts to Ventoy
cp -r scripts/debian/debian_install.sh /media/geoff/Ventoy/scripts/debian/debian_install.sh
cp -r scripts/debian/preseed.cfg /media/geoff/Ventoy/scripts/debian/preseed.cfg
cp -r scripts/debian/postinstall.service /media/geoff/Ventoy/scripts/debian/postinstall.service

# Copy Raspberry Pi scripts to Ventoy
cp -r scripts/raspberrypi/raspberrypi_install.sh /media/geoff/Ventoy/scripts/raspberrypi/raspberrypi_install.sh
