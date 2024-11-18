#!/bin/env python3 

from re import sub
from dns import exception
import dns.zone as dz 
import dns.query as dq 
import dns.resolver as dr 
import argparse 

S = '\033[92m[+]\033[0m ' # Success (green)
I = '\033[93m[!]\033[0m ' # Information (yellow)
F = '\033[91m[X]\033[0m ' # Failure (Red)


domain = 'inlanefreight.htb'
NS = dr.Resolver()
NS.nameservers = []
subdomains = [] 
filtered_subdomains = [] 

def resolve_nameserver_to_IP(nameserver):
    """dq.xfr() will expect an the IP address of the nameservers, this function 
       resolves the IP address of the nameservers."""
    try:
       answer = dr.resolve(nameserver, 'A')
       return str(answer.nameserver)
    except Exception as error:
        print("Error resolving nameservers: \n", error)
        return 0


def AXFR(nameserver, domain): 
    try:
        axfr = dz.from_xfr(dq.xfr(nameserver, domain))
        if axfr:
            print(f'Successful Zone Transfer from {nameserver}')
            for record in axfr:
                if (record.to_text() + f'.{domain}') not in subdomains:
                    subdomains.append(record.to_text() + f'.{domain}') 
            return True 
        return False 

    except Exception as error:
        print('error occurred', error)
        pass

if __name__ == '__main__':

    parser = argparse.ArgumentParser(epilog='DNS Zonetransfer Script',
                                     usage='./dns-zone-transfer.py [options] -d domain',
                                     prefix_chars='-',
                                     add_help=True)

    parser.add_argument('-d', '--domain', action='store', metavar='Domain', 
                        type=str, 
                        required=True,
                        help='Target domain.\t Example: Domain.com')

    parser.add_argument('-n', '--nameserver', action='store', metavar='Nameserver', 
                        type=str,
                        required=False,
                        help='Nameservers separated by a comma.\tExample: ns1.domain.com,ns2.domain.com')

    parser.add_argument('-v', '--version', action='version', version='dns-zone-transfer V1.0', 
                        help='Prints the current version.')

    args = parser.parse_args()
    domain = args.domain

    # Get nameservers 
    nameservers = dr.resolve(domain, 'NS')
    for ns in nameservers:
        print(I + "Found Nameserver:", str(ns).rstrip('.'))
        NS.nameservers.append(str(ns).rstrip('.'))

    # TODO: figure out how to get the correct IP for each NS
    # Resolve nameservers to IPs 
    for nameserver in NS.nameservers:
        nameserver_ip = resolve_nameserver_to_IP(nameserver)
        print("Current nameserver:", nameserver_ip)
        #AXFR(IP, domain)

    # The domain is in the subdomains list, so we subtract 1 
    print(f"[!] Found {len(subdomains)-1} unique subdomains!!!\n")
    for subdomain in subdomains:
        print(subdomain)
