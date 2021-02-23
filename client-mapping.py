#!/usr/bin/env python

# Updated to support pyunifi library and pi-hole 5.0 custom.list instead of hosts by default. Master branch hardcoded to ssl_verify=False

import argparse, string, os, sys
from netaddr import *
from unifi_controller_ext import ControllerExt
from python_hosts import HostsEntry
from pihole_hosts import PiHoleHosts

parser = argparse.ArgumentParser(description = "Fetch list of hosts from unifi controller and place them in a hosts file")
parser.add_argument('-v', '--verbose', action='store_true', help = "print additional information")

parser.add_argument('-nh', '--nohosts', action='store_true', help = "don't attempt to write to hosts file")
parser.add_argument('-m', '--mixedcase', action='store_true', help = "do not force all names to lower case")
parser.add_argument('-d', '--domains', action='store_true', help='adds domain name from unifi network if exists')

parser.add_argument('-f', '--hostfile', help = "hosts file to use", default = "/etc/pihole/custom.list")
parser.add_argument('-c', '--controller', help = "controller IP or hostname")
parser.add_argument('-u', '--user', help = "username")
parser.add_argument('-p', '--password', help = "password")
args = parser.parse_args()

if args.verbose:
    print args

if args.controller is not None:
    controllerIP = args.controller
else:
    controllerIP = os.getenv("UNIFI_CONTROLLER")
    if controllerIP is None:
        controllerIP = raw_input('Controller: ')
if args.verbose:
    print "Using controller IP %s" % controllerIP

if args.user is not None:
    userName = args.user
else:
    userName = os.getenv("UNIFI_USER")
    if userName is None:
        userName = raw_input('Username: ')
if args.verbose:
    print "Using username %s" % userName

if args.password is not None:
    password = args.password
else:
    password = os.getenv("UNIFI_PASSWORD")
    if password is None:
        password = raw_input('Password: ')

c = ControllerExt(controllerIP, userName, password, "8443", "v4", "default", ssl_verify=False)
clients = c.get_clients()
useDomains = args.domains
if not useDomains:
    useDomains = os.getenv("USE_UNIFI_DOMAINS") <> None

if useDomains:
    domains = c.get_network_domains()
else:
    domains = dict()

list = {}

if args.verbose:
    print "Using hosts file %s" % args.hostfile
hosts = PiHoleHosts(path=args.hostfile)

for client in clients:
    ip = client.get('ip', 'Unknown')
    hostname = client.get('hostname')
    name = client.get('name', hostname)
    if name:
        name = unicode.strip(name)
    if not args.mixedcase and name <> None:
        name = name.lower()
    network_id = client['network_id']
    domain = domains.get(network_id)
    if domain:
        unicode.strip(domain)
    if domain and name:
        name = name + '.' + domain
    mac = client['mac']

    if ip <> "Unknown":
        ip = IPAddress(ip)

    if ip <> "Unknown" and name:
        name = name.replace(" ", "")
        list[ip] = name
        sorted(list)

for entry in list.items():
    ip = str(entry[0])
    name = entry[1]
    new_entry = HostsEntry(entry_type='ipv4', address=ip, names=[name])

    if hosts.exists(ip):
      hosts.remove_all_matching(ip)

    hosts.add([new_entry])
    if args.verbose:
        print entry[0], entry[1]

if args.verbose:
    if args.nohosts:
        print "--nohosts specified, not attempting to write to hosts file"

if not args.nohosts:
    try:
        hosts.write()
    except:
        print "You need root permissions to write to /etc/hosts - skipping!"
        sys.exit(1)
