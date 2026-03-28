#!/bin/bash

BASE_DIR="/device_provision"
LOG_DIR="$BASE_DIR/logs"

source "$BASE_DIR/device.env"

mkdir -p "$BASE_DIR/repo" "$LOG_DIR"

exec 9>"$BASE_DIR/.pull.lock"

flock -n 9 || exit 0

/usr/bin/ansible-pull \
  -U "$REPO_URL" \
  -C "$BRANCH" \
  -d "$BASE_DIR/repo" \
  -i "$INVENTORY_FILE" \
  "$PLAYBOOK" \
  >> "$LOG_DIR/ansible-pull.log" 2>&1
