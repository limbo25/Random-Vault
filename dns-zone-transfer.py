#!/bin/env python3 

from re import sub
from dns import exception
import dns.zone as dz 
import dns.query as dq 
import dns.resolver as dr 
import argparse 

IP = '10.129.240.120'
domain = 'inlanefreight.htb'
NS = dr.Resolver()
NS.nameservers = []
subdomains = [] 

def resolve_nameserver_to_IP(nameserver):
    """dq.xfr will expect an the IP address of the nameservers, this function 
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
            print('Successful Zone Transfer from {}'.format(nameserver))
            for record in axfr:
                subdomains.append('{}.{}'.format(record.to_text(), domain)) 
    except Exception as error:
        print('error occurred', error)
        pass

if __name__ == '__main__':
    nameservers = dr.resolve('inlanefreight.com', 'NS')
    for ns in nameservers:
        NS.nameservers.append(str(ns).rstrip('.'))

    for nameserver in NS.nameservers:
        nameserver_ip = resolve_nameserver_to_IP(nameserver)
        print("\n\nCurrent nameserver:", nameserver_ip)
        #AXFR('10.129.240.120', 'inlanefreight.htb')
        AXFR(IP, domain)

    











