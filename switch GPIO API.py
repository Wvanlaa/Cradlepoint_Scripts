"""
Author: Wim van Laarhoven
Date 28-02-2023
Version: Generic PoC/Test
Switch GPIO on and off to switch external power-source.
Based on original GPIO demo script, but increased "wait" timer to 20 seconds to allow for stable running.

Use Script:
- fill out the correct API information in the "headers section"
- get the router-ID from NCM for the designated router, and fill that out here: "router.id=xxxxxxx"
- Change the "pin number" where appropriate. Power-cable GPIO is "pin 0"
- run the script without arguments

Router Configuration:
- System / GPIOs
- Enable GPIO ("1 on power cable" is enabled by default)
- GPIO Name:            Relay
- Open State Name:      off
- Closed State Name:    on
- Alert Trigger State:  Both
- Action:               Off (Default)

Further information also here: https://customer.cradlepoint.com/s/article/Cradlepoint-GPIO-Reference

TODO: 
- Would be nice if the script would accept the NCM Router ID / Serial Number and/or Pin number as argument.
- check if router is online and provide proper error handling
- check if router is in "sync suspended"

"""

import json
from urllib.request import Request, urlopen
import requests
import sys
import time

# Enter the pin-number here:
pinnr = '0'
# Enter the RouterID from NCM from the "ID" column in the Devices view
ncmrouterid = '--<routerID goes here>--'

# NCM Headers for REST API - Wim Main Account
headers = {'X-CP-API-ID': '--< YOUR >--',
        'X-CP-API-KEY': '--< KEYS >--',
        'X-ECM-API-ID': '--< GO >--',
        'X-ECM-API-KEY': '--< HERE >--',
        'Content-Type': 'application/json'
        } 
        
print('Power OFF/ON Media Server')

# Obtain the configuration ID of the router by querying the device configuration
config_url = 'https://cradlepointecm.com/api/v2/configuration_managers/?router.id=' + ncmrouterid + '&fields=id'
config_req = Request(config_url, headers=headers)
config_response = urlopen(config_req)
configJSON = json.loads(config_response.read().decode())
conf_id = configJSON['data'][0]['id']

# Create the URL and configuration for writing to the router
write_url = 'https://cradlepointecm.com/api/v2/configuration_managers/' + conf_id + '/?fields=configuration'
payload = {"configuration":[{"system": {"gpio_actions": {"pin": {pinnr: {"current_action": "out_action_high"}}}}},[]]}
payloadprime = json.dumps(payload, indent=4)
print('GPIO pin set to: {} (off)'.format(payload['configuration'][0]['system']['gpio_actions']['pin'][pinnr]['current_action']))

# Send patch configuration to the router to power off the power strip
requests.patch(write_url, data = payloadprime, headers = headers)

# Wait 20 seconds before powering back on
print('Waiting 20 seconds to power back on')
time.sleep(20)

# Create the URL and configuration for writing to the router
payload = {"configuration":[{"system": {"gpio_actions": {"pin": {pinnr: {"current_action": "out_action_low"}}}}},[]]}
payloadprime = json.dumps(payload, indent=4)
print('GPIO pin set to: {} (on)'.format(payload['configuration'][0]['system']['gpio_actions']['pin'][pinnr]['current_action']))

# Send patch configuration to the router to power on the power strip
requests.patch(write_url, data = payloadprime, headers = headers)