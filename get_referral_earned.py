#!/usr/bin/env python3
import runpod
import json
from colorama import Fore, Style, init


if __name__ == '__main__':
    runpod = runpod.API()
    response = runpod.get_myself()
    resp_json = response.json()

    if response.status_code == 200:
        myself = resp_json['data']['myself']
        referral_earned = myself.get('referralEarned')
        template_earned = myself.get('templateEarned')
        total_earned = referral_earned + template_earned

        init(autoreset=True)

        print(f"{Fore.CYAN}  Referral Earned: {Fore.CYAN}{referral_earned}")
        print(f"{Fore.CYAN}  Template Earned: {Fore.CYAN}{template_earned}")
        print(f"{Fore.LIGHTGREEN_EX}  Total Earned:    {Fore.LIGHTGREEN_EX}{total_earned}{Style.RESET_ALL}")
    else:
        print('ERROR:')
        print(f'Status code: {response.status_code}')
        print(json.dumps(resp_json, indent=4, default=str))
