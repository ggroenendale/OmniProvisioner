## Configuring a fresh Debian server:

Our goal is to determine the exact things we need to place, install, or configure on a fresh Debian
install in order to enable it to run `ansible-pull` and configure the remainder of the packages
necessary for that specific machine.

This list will definitely include ansible and at least one shell script to run with cron every
set amount of time.

### Pre) What does a Fresh Debian Server have?

After install, you typically have:

- bash
- apt
- systemd
- cron
- ssh

### 1) Install Required System Packages

```bash
apt update
apt install -y ansible git python3 python3-apt
```

Why each matters:

| Package     | Why                             |
| ----------- | ------------------------------- |
| ansible     | Provides ansible-pull           |
| git         | Required to clone repo          |
| python3     | Ansible runs on Python          |
| python3-apt | Required for apt module to work |

> Note: If you forget python3-apt, package installs will fail.
> That’s the most common “fresh Debian” mistake.

### 2) Create a user specifically for provisioning

```bash
useradd -r -m -d /device_provision -s /bin/bash provisioner
chown -R provisioner:provisioner /device_provision
```

### 3) Setup Inventory File - /etc/ansible/hosts

This file is specific to each configuration, therefore it is something we can save in the repository but it needs
to be copied to the machine during or post-install.

Example for a k3s node:

```ini
[k3s]
k3s1

[all]
k3s1 ansible_connection=local
```

Example for a router:

```ini
[router]
router1

[all]
router1 ansible_connection=local
```

### 4) Define device Hostname to match the Inventory Name

> The hostname of the device must match the inventory name in ansible. This may be configured differently depending
> on the operating system configured. For example this may work differently on OpenSUSE than it does on Debian.
> However given that this documentation is specifically for Debian we won't worry about that.

```bash
hostnamectl set-hostname k3s1
```

### 5) Create the Pull Script shell file

Create a shell file here: `/usr/local/bin/homelab-pull.sh`

With the contents:

```bash
#!/bin/bash

BASE_DIR="/device_provision"
REPO_DIR="$BASE_DIR/repo"
LOG_DIR="$BASE_DIR/logs"

ANSIBLE_PULL="/usr/bin/ansible-pull"
REPO_URL="https://<git-host>/<git-repository-name>.git"
BRANCH="main"
PLAYBOOK="homelab.yaml"
INVENTORY="/etc/ansible/hosts"

mkdir -d -p "$REPO_DIR" "$LOG_DIR"

$ANSIBLE_PULL \
  -U "$REPO_URL" \
  -C "$BRANCH" \
  -d "$REPO_DIR" \
  -i "$INVENTORY" \
  "$PLAYBOOK" \
  >> "$LOG_DIR/ansible-pull.log" 2>&1
```

Change the owner and make it executable

```bash
chown provisioner:provisioner /device_provision/homelab-pull.sh
chmod 750 /device_provision/homelab-pull.sh
chmod +x /usr/local/bin/homelab-pull.sh
```

### 6) Configure systemd service

First create service file: `/etc/systemd/system/homelab-pull.service`

With the contents

```ini
[Unit]
Description=Homelab Ansible Pull

[Service]
Type=oneshot
User=provisioner
WorkingDirectory=/device_provision
ExecStart=/device_provision/homelab-pull.sh
```

Then create the timer file: `/etc/systemd/system/homelab-pull.timer`

With the contents

```ini
[Unit]
Description=Run Homelab Pull every 15 minutes

[Timer]
OnBootSec=2min
OnUnitActiveSec=15min

[Install]
WantedBy=timers.target
```

> Note: So long as the .service and .timer share the same base file name, the timer
> will run the service file.

Then enable it:

```bash
systemctl daemon-reload
systemctl enable --now homelab-pull.timer
```
