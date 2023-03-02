import requests
import json
import argparse

with open('config.json') as file:
    CONFIG = json.load(file)

def main(args):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {CONFIG['apikey']}" 
    }

    payload_power_on = {
        'boot': True,
    }
    payload_power_off = {
        'boot': False,
    }
    payload_reboot = {
        'boot': True,
        'config_id': None,
    }

    power_on_url = f"{CONFIG['apiurl']}/linode/instances/{args.id}/boot"
    power_off_url = f"{CONFIG['apiurl']}/linode/instances/{args.id}/shutdown"
    restart_instance = f"{CONFIG['apiurl']}/linode/instances/{args.id}/reboot"


    if args.power == 'start':
        response = requests.post(power_on_url, headers=headers, data=json.dumps(payload_power_on))
        if response.status_code == 200:
            print(f"[ + ] Linode instance {args.id} is now Powering up")
        
        elif response.status_code == 400:
            print(f"[ ! ] Linode instance {args.id} is already running!")

        else:
            print(f"[ - ] Error: {response.status_code}")

    elif args.power == 'stop':
        response = requests.post(power_off_url, headers=headers, data=json.dumps(payload_power_off))
        if response.status_code == 200:
            print(f"[ + ] Linode instance {args.id} is now powering off")
        else:
            print(f"[ - ] Error: {response.status_code}")

    elif args.power == 'restart':
        response = requests.post(restart_instance, headers=headers, data=json.dumps(payload_reboot))
        if response.status_code == 200:
            print(f"[ * ] Linode instance {args.id} is rebooting...")
        else:
            print(f"[ - ] Error: {response.status_code}")


if '__main__' == __name__:
    parser = argparse.ArgumentParser(description='A basic script just to interact with the Linode instances')
    parser.add_argument('-i', '--id', dest='id', help='The instance ID (Ex: -i 12345678)', type=int, required=True)
    parser.add_argument('-p', '--power', dest='power', help='Power up or down a Linode instance', type=str, choices=['start', 'restart', 'stop'], default='', required=True)
    args = parser.parse_args()

    main(args)
