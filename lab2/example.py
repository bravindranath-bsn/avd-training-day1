import requests
from jinja2 import Environment, FileSystemLoader
from pprint import PrettyPrinter

# disable warnings about self-signed certs
import urllib3
urllib3.disable_warnings()

DEVICE_IPS = ['192.168.0.10',
              '192.168.0.11',
              '192.168.0.12',
              '192.168.0.13',
              '192.168.0.14',
              '192.168.0.15',
              '192.168.0.16',
              '192.168.0.17'
              ]
              
# USE YOUR CREDENTIALS
USERNAME = 'arista'
PASSWORD = 'aristaivm8'

if __name__ == '__main__':
    payload = {'jsonrpc': '2.0',
               'method': 'runCmds',
               'params': {
                 'version': 1,
                 'cmds': ['show version',
                          'show hostname',
                          'show ip arp']
               },
               'id': '1'
              }
    device_outputs = {}

    pp = PrettyPrinter()
    env = Environment(loader=FileSystemLoader("/home/coder/project/labfiles/day1/lab2/"))
    template = env.get_template("example.j2")

    for device in DEVICE_IPS:
        r = requests.post('https://{}:443/command-api'.format(device), json=payload, auth=(USERNAME, PASSWORD), verify=False)
        response = r.json()
        #pp.pprint(response)

        device_outputs[response['result'][1]['hostname']] = {'serial': response['result'][0]['serialNumber']}
        #figure out how to store the ARP address table data in a way that will make your template rendering easy
        
        device_outputs[response['result'][1]['hostname']]['total_arp'] = response['result'][2]['dynamicEntries']
        device_outputs[response['result'][1]['hostname']]['arp_table'] = response['result'][2]['ipV4Neighbors']
    else:
        #pp.pprint(device_outputs)
        print(template.render(devices=device_outputs))