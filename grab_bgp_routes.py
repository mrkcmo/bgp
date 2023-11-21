''' This script is for grabbing routes from a single device and exporting them into a CSV file '''
import argparse
from netmiko.ssh_autodetect import SSHDetect
from netmiko import ConnectHandler
from getpass import getpass
import textfsm
from tabulate import tabulate


class GetRoutes():
    def __init__(self, device, username, password, verbose):
        self.device = device
        self.username = username
        self.password = password
        self.verbose = verbose

    def connectDevice(self):
        remote_device = {
            'device_type': 'autodetect',
            'host': self.device,
            'username': self.username,
            'password': self.password,
            'secret': self.password
        }

        guesser = SSHDetect(**remote_device)
        best_match = guesser.autodetect()
        if verbose:
            print(best_match)
            print(guesser.potential_matches)
        remote_device["device_type"] = best_match

        with ConnectHandler(**remote_device) as net_connect:
            net_connect.enable()
            prompt = net_connect.find_prompt()
            prompt = prompt.replace('#', '')
            net_connect.send_command('terminal length 0')
            routes = net_connect.send_command('show ip bgp')

            if 'cisco_ios' or 'cisco_xe' in best_match:
                template = './templates/cisco_ios_show_ip_bgp.textfsm'
            elif 'cisco_nxos' in best_match:
                template = './templates/cisco_nxos_show_ip_bgp.textfsm'
            output_file = prompt + '-results.csv'

            with open(template) as f, open(output_file, 'w+') as output:
                re_table = textfsm.TextFSM(f)
                header = re_table.header
                result = re_table.ParseText(routes)
                if verbose:
                    print(result)
                    print(tabulate(result, headers=header))
                output.write(tabulate(result, headers=header))
                output.close()

            net_connect.disconnect()


if __name__ == "__main__":
    ''' Main Function Call to Start the Script '''
    parser = argparse.ArgumentParser(prog='Get BGP Routes',
                                     description='This script will log into the device and grab the BP routes and parse them into a CSV file.',
                                     epilog='Created by Chris Fortner')
    parser.add_argument('-u', '--username', required=True)
    parser.add_argument('-d', '--device', required=True)
    parser.add_argument('-v', '--verbose', action='store_true', required=False)

    args = parser.parse_args()

    username = args.username
    device = args.device
    verbose = args.verbose
    password = getpass()
    run = GetRoutes(device, username, password, verbose)
    run.connectDevice()
