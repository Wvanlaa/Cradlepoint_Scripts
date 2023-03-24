#!/usr/bin/python3

"""
Author:     Wim van Laarhoven
Date:       24-03-2023
Version:    1.0

Usage:      - Run the script with the default admin password as argument
            - change the apndata field to represent the intended APN

Function:
The function of this specific script is to set the APN to Manual and add a custom APN
"""


import sys
import requests

argpassword = str(sys.argv[1])
print (argpassword)

router_url = 'http://192.168.0.1/api'
auth=('admin', argpassword)
apnmode = "manual"

# change the APN here:
apndata = "internet"

# Main change
req = requests.put(f'{router_url}/config/wan/rules2/2/modem/apn_mode', data={"data": f'"{apnmode}"'}, auth=auth)
print(req.text)
req = requests.put(f'{router_url}/config/wan/rules2/2/modem/manual_apn', data={"data": f'"{apndata}"'}, auth=auth)
print(req.text)