"""Export NCM API Usage_Samples/ data to .csv file.

This script will export the data from the Cradlepoint NCM API
Usage_Samples/ endpoint for all network devices for the given date range.
Just net_devices with a type of "mdm" are used has to have an iccid
Data is written to the .csv file defined below.
Cradlepoint NCM API keys are required.

Attributes
----------
start_date : beginning of date range to export
end_date : end of date range to export
output_file : name of .csv file to be created
headers : Replace values with your NCM API keys for use in HTTP requests.

notes: 
    - cannot use __lte in end_date, so __lt is used. That means in order to get today values, the end_date needs to be in the future
    - for period and uptime Linux Epoch time is used (in seconds) and the value left of the "." should be sufficient to do all calculations

"""

import requests
import csv

start_date = '2024-09-29'
end_date = '2024-09-30'

output_file = 'UsageSamples.csv'

"""
headers = {'X-ECM-API-ID': 'Your',
           'X-ECM-API-KEY': 'Keys',
           'X-CP-API-ID': 'Go',
           'X-CP-API-KEY': 'Here',
           'Content-Type': 'application/json'}
"""

headers = {'X-ECM-API-ID': 'Your',
           'X-ECM-API-KEY': 'Keys',
           'X-CP-API-ID': 'Go',
           'X-CP-API-KEY': 'Here',
           'Content-Type': 'application/json'}


top_line = ["net_deviceID", "net_device_name", "Router_name", "iccid", "bytes_in", "bytes_out",
            "created_at", "created_at_timeuuid", "net_device", "period",
            "uptime"]


server = 'https://www.cradlepointecm.com'

with open(output_file, 'w', newline='' ) as f:
    writer = csv.writer(f, delimiter=',')
    writer.writerow(top_line)  # write header

    net_devices_url = f'{server}/api/v2/net_devices/?' \
        f'&limit=500'
    try:
        while net_devices_url:
            net_devices_req = requests.get(net_devices_url, headers=headers).json()
            net_devices = net_devices_req['data']
            for net_device in net_devices:
                # print(net_device["type"])
                if net_device["type"]=="mdm":              
                    samples_url = f'{server}/api/v2/net_device_usage_samples/' \
                        f'?net_device={net_device["id"]}&created_at__gt={start_date}' \
                        f'&created_at__lt={end_date}'
                    while samples_url:
                        samples_req = requests.get(
                            samples_url, headers=headers).json()
                        print(f'Modem ID: {net_device["id"]} Usage Samples: '
                            f'{samples_req["data"]}')
                        samples = samples_req['data']
                        for sample in samples:
                            if net_device['iccid']:
                                loc_values = [x for x in sample.values()]
                                row = [net_device["id"], net_device["name"], net_device["hostname"], net_device["iccid"]] + loc_values
                                writer.writerow(row)
                        samples_url = samples_req['meta']['next']
            net_devices_url = net_devices_req['meta']['next']
    except Exception as e:
        print(e)
