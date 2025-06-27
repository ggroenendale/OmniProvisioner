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

# Copy the Ansible repo into the installed system this should be cloned during the
# archinstall configuration
echo "Cloning OmniProvisioner into /mnt/root/"
arch-chroot /mnt git clone https://github.com/ggroenendale/OmniProvisioner.git /root/OmniProvisioner

# We should be able to move the .vault_pass.txt file into our OmniProvisioner folder
mv .vault_pass.txt /mnt/root/OmniProvisioner/

# Create the systemd service unit inside /mnt
cat <<EOF > /mnt/etc/systemd/system/firstboot-ansible.service
[Unit]
Description=First Boot Ansible Provisioning
After=network.target

[Service]
Type=oneshot
ExecStart=/root/run-ansible.sh
RemainAfterExit=true

[Install]
WantedBy=multi-user.target
EOF

echo "Systemd service created in /mnt/etc/systemd/system"

# 4️⃣ Create the ansible runner script inside /mnt
cat <<EOF > /mnt/root/run-ansible.sh
#!/bin/bash
set -e

echo "Running first-boot Ansible provisioning"
ansible-playbook -i localhost, /root/OmniProvisioner/playbooks/desktop.yaml

echo "Provisioning complete. Disabling service."
systemctl disable firstboot-ansible.service
EOF

chmod +x /mnt/root/run-ansible.sh
echo "Runner script installed in /mnt/root/"

# 5️⃣ Enable the service in the installed system
arch-chroot /mnt systemctl enable firstboot-ansible.service

echo "First-boot Ansible service enabled in installed system"

echo "Installation complete, reboot and ansible will run the first configuration"
