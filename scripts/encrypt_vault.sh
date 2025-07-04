# Encrypt several files in one go
ansible-vault encrypt roles/arch_desktop/vars/user_uncry.yaml --output roles/arch_desktop/vars/user_encr.yaml
#ansible-vault decrypt roles/arch_desktop/vars/user_uncry.yaml

#ansible-vault encrypt roles/arch/vars/secrets.yml
#ansible-vault encrypt roles/arch/vars/db_passwords.yml

