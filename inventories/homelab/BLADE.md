# Laptop Blade Server Install

## Introduction

The purpose of this role is to run debian on a laptop and have it join a k3s cluster. Eventually my goal is to take the laptop motherboards out of their
plastic cases and put them into a rack mountable chassis.

We will likely continue to use their current power supply bricks, however we might be able to make custom power supply boards in the future.

The laptops should by default disable any laptop lid closed issues. And we will remove the batteries as they are a fire hazard. We can use a proper UPS and battery back up in the future.

For now we will

## Overview

### Laptop Inventory

#### 1) Dell

Model: PP29L
P/N UK530 A00
Input: 19.5Vdc 3.34A

Processor: Intel Dual Core T3400 processor at 2.16GHz
RAM: 4GB

#### 2) Gateway

Model: MA8
Input: 19Vdc 3.42A

Processor: Pentium T2310 1.46 GHz
RAM: 1GB

#### 3) HP Elitebook

Model: Elitebook 840 G3
SKU: X7R86EC#ABA

Processor: Intel Core i5-6300U CPU 2.4GHZ dual core
RAM: 16GB RAM (possibly upgrade to 32GB)
GPI: Intel HD Graphics 520

#### 4) HP

Model: 15-dy0013dx
ProdID: 7FU54UA#ABA
S/N: 5CD9450TG2
Input 19.5Vdc 2.31A

Processor: Intel Core i5-8265U (6MB Cache, 1.6GHz) quad core
RAM: 16GB (2400MHz) DDR4-SDRAM (possibly upgrade to 32GB)
GPU: Intel HD Graphics 620

#### 5) Lenovo

Model: Ideapad 310-15IKB
Model Name: 80TV
S/N:PF0PY5SJ
Input: 20Vdc 2.25A

Processor:Intel Core i5 (7th Gen) 7200U / 2.5 GHz dual core
RAM: 12GB max 2133MHZ (1-8GB stick + 4GB soldered)
GPU: Intel HD Graphics 620

#### 6) Toshiba

Model: A505-S6005
Part No.: PSAT6U-005002
S/N: Z9238422Q

Processor: Intel Core i3-330M Processor 2.13 GHz, 3MB L3 Cache
RAM: 8GB

#### 7) Toshiba

Model: Satellite A215-S4807
Part No.: PSAEGU-01400U
S/N: 77300364K
Input: 19Vdc 3.95A

Processor: AMD Turion X2 TL-56 1.80 GHz Dual-core (2 Core)
RAM: Max 4GB

### Services and Packages

List of packages and services to install

- k3s
- File Storage

## Installation

Installation step by step:

### Setup PXE boot server

### Connect laptop to network

### Boot to laptop BIOS and enable netboot

### Install Debian image to laptop
