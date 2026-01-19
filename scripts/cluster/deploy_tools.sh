#!/bin/bash

# Make a variable for the working directories of the project
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
PROJ_DIR="$SCRIPT_DIR"

# Spin up Zot Registry
# helm repo add project-zot http://zotregistry.dev/helm-charts
#
# helm search repo project-zot
#
# helm repo update project-zot
#
# helm install zot project-zot/zot

# # Spin up Gitea
# helm repo add gitea-charts https://dl.gitea.com/charts/
# helm repo update gitea-charts
#
# kubectl create namespace gitea
#
# helm upgrade --install gitea gitea-charts/gitea --namespace gitea -f "$SCRIPT_DIR/gitea-values.yaml"
#
# # Spin up Woodpecker CI
# helm repo add woodpecker oci://ghcr.io/woodpecker-ci/helm
# helm repo update woodpecker
#
# kubectl create namespace woodpecker
#
# helm upgrade --install woodpecker woodpecker/woodpecker --namespace woodpecker -f "$SCRIPT_DIR/woodpecker-values.yaml"

# Connect woodpecker to kubernetes so it can deploy on kubernetes
# Create a service account for woodpecker
# kubectl create serviceaccount woodpecker-deployer
#
# # Give it access to the entire cluster to create any resource
# kubectl create clusterrolebinding woodpecker-deployer-binding \
#   --clusterrole=cluster-admin \
#   --serviceaccount=default:woodpecker-deployer

# Next we get the token and ca cert
SECRET=$(kubectl get sa woodpecker-deployer -o jsonpath='{.secrets[0].name}')

# Extract token
TOKEN=$(kubectl get secret $SECRET -o jsonpath='{.data.token}' | base64 -d)

# Extract cluster CA cert
CA=$(kubectl get secret $SECRET -o jsonpath='{.data.ca\.crt}')

# Get API server address
SERVER=$(kubectl config view --minify -o jsonpath='{.clusters[0].cluster.server}')


echo "Secret: $SECRET"
echo "Token: $TOKEN"
echo "CA: $CA"
echo "Server $SERVER"


# Spin up Gitlab
# helm repo add gitlab https://charts.gitlab.io
# helm repo update gitlab
#
# kubectl create namespace gitlab
#
# helm upgrade --install gitlab gitlab/gitlab --namespace gitlab -f "$SCRIPT_DIR/gitlab-values.yaml"
#helm upgrade --install gitlab gitlab/gitlab --namespace gitlab 
