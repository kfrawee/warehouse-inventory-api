# Warehouse Inventory API 🏪
A python-based solution for a Warehouse Inventory system.

## Overview:

A shop in London has 2 million IoT tracking devices in the Warehouse Inventory for sale,
of which half need configuration to meet UK industry standards.
A configured device will have a status ACTIVE and an ideal temperature between (0’C to
10’C).

When a device is not configured, the default status is READY and temperature value is -
1’C.

Every device has a unique secret seven-digit pin code used for unlocking the device.
A given device needs to be sent to a Device Configuration Service (DCS) to set the device
status ACTIVE and random temperature value between (0 to 10).
The Device Configuration Service does not need a device pin code for the configuration
operation.

The shop can sell a device only if it meets the UK government's industry standard.

## The project includs (Task):
Develop a solution for the London shop as described above:
1. Develop a REST API for the Warehouse Inventory to
    - Add, update, or remove a device
    - Return all devices available for sale in numerical order of their seven-digit
pin code.
2. Develop the Device Configuration Service and provide an endpoint responsible for configuring a device.
3. Provide comprehensive Unit and Integration tests for
    - All database repositories where applicable,
    - All communicating API and endpoints.

## How to use:
[WIP]
