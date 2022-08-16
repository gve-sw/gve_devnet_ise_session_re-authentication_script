# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright (c) 2022 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
               https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

__author__ = "Trevor Maco <tmaco@cisco.com>"
__copyright__ = "Copyright (c) 2022 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"


# Imports
from dotenv import load_dotenv
from datetime import datetime
import sys
import os
import csv

from concurrent.futures import ThreadPoolExecutor, as_completed

from netmiko import ConnectHandler

# load environment variables
load_dotenv()

# global variables
SWITCH_USERNAME = os.getenv("SWITCH_USERNAME")
SWITCH_PASSWORD = os.getenv("SWITCH_PASSWORD")
MAX_THREADS = int(os.getenv("MAX_THREADS")) 


# Read csv data
def read_csv(filename):

    print(f'Reading {filename}...')

    with open(filename, 'r') as file:
        csv_data = csv.DictReader(file)

        # Extract each row of data (representing an effected device)
        devices = []
        for device in csv_data:
            devices.append(device)

    print(f'{filename} successfully read')

    return devices


# Clear authentication session on each connected device and port
def clear_auth_session(device):

    # The connected switch
    switch = {
        "device_type": "cisco_ios",
        "ip": device['NAS-IP-Address'],
        "username": SWITCH_USERNAME,
        "password": SWITCH_PASSWORD,
    }

    # Connected port on the switch-side
    target_port = device['NAS-Port-Id']

    # Authentication command strings    
    clear_command = f"clear auth sessions int {target_port}"
    
    try:
        print(f"Clearing session for: {device['MACAddress']}")
        print(
            f"Connecting to: Switch IP ({device['NAS-IP-Address']}) , Switch Port ({device['NAS-Port-Id']})")

        # Establish a SSH connection to the switch
        c = ConnectHandler(**switch)

        print('Successfully connected...')

        # Enter privilege mode
        c.enable()

        # Send the clear_command to be executed
        response = c.send_command(clear_command)
        
        # Disconnect the SSH session
        c.disconnect()

    except Exception as e:
        response = e

    finally:
        return (device, response)


# Output the results of the clear session command on each switch to console and log file
def output_results(device, response):
    
    # print to console 
    print("*" * 50 + "\n")
    print(f"{device['MACAddress']} has finished processing!")
    print('Result: \n')

    if isinstance(response, Exception):
        print(str(response))
    else:
        # If successful, result will be None (changed for readability), otherwise results will contain text printed to console
        if response is None:
            print('Successfully cleared!')
        else:
            print(response)

    

def main():

    # Sanity checking a csv file was provided
    if len(sys.argv) != 2 or not sys.argv[1].endswith('.csv'):
        print('Error: please input a valid.csv file')
        exit()

    # filename is set from CLI argument
    filename = sys.argv[1]

    # Read in CSV Data
    devices = read_csv(filename)

    # Create a 'thread pool', this allows us to run multiple threads (up to max_workers), where each 'thread' is a ssh connection and execution of the clear session command on a switch.
    # Threading allows us to multitask and kick off the command on multiple switches simultaneously, dramatically increasing speed at scale!
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        result_list = []

        # Iterate through list of affected devices
        for device in devices:

            print(f"Adding {device['MACAddress']} to thread queue...")

            # Add each device to it's own thread
            future = executor.submit(clear_auth_session, device)
            result_list.append(future)

        # As results come in and threads terminate, output to console and write results to log file
        for result in as_completed(result_list):
            device, response = result.result()

            output_results(device, response)
    
    print('All switches processed!')



if __name__ == "__main__":
    main()
