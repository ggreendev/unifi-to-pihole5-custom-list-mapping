### unifi-to-custom-list-mapping for pi-hole 5.0 - beta

This version currently fails - please use Master Branch

4th May 2020: Updated to support pyunifi library as unifi library is unsupported.
4th May 2020: Updated to support pi-hole 5.0 custom.list instead of hosts file 

Within the UniFi controller you can create an alias for devices as they appear on the network. This script takes the alias entries and their corresponding IP address to maintain a list of Custom DNS entries on the PiHole server. These entries reside in /etc/pihole/custom.list which can be accessed and viewed via the PiHole UI under "Custom DNS". The end result is the dashboard showing your configured hostname for Top Clients and not just an IP Address. 

Place script on PiHole server, in my case this is in /home/pi. You will also need to ensure you have the relevant python libraries installed. 

Note: I am using an adjusted hosts.py file to enable support for spaces instead of tabs in the host file creation - you will need to replace the hosts.py file created by python_hosts with the one here. See below for instructions.

```
sudo pip install python_hosts
sudo pip install pyunifi
sudo pip install netaddr

```
The script requires the controller IP (or hostname), controller username and password to function correctly.  You can specify each of these via a command line parameter (`-c`, `-u` and `-p`), an environment variable (`UNIFI_CONTROLLER`, `UNIFI_USER` and `UNIFI_PASSWORD`), or interactively (in that order of precedence). You can also revert and adjust this to write to a different hosts file instead of the new custom.list (or if your custom.list is in a different directory), using ('-f'). e.g. -f /etc/hosts

Still in the works: 
It will also support verification of an SSL Certificate using command line parameter ('-s') or an environment variable ('SSL_CERT_VAR'), with options True, False or defining path to specific certificate "path/to/custom_cert.pem". I have defaulted it to False which is opposite to pyunifi library.

Create a suitable crontab entry for the root user, it will need to be for the root user as you are modifying the /etc/hosts file. 

```
sudo crontab -e 

Add the following lines to the cron file and save/exit

0,15,30,45 * * * * /home/pi/client-mapping.py
```
If not using environment variables, use:
```
sudo crontab -e 

Add the following lines to the cron file and save/exit

0,15,30,45 * * * * /home/pi/client-mapping.py -c [Controller IP] -u [Controller username] -p [Controller password]
```
=====

hosts.py

To replace this, please copy this new version to /usr/local/lib/python2.7/dist-packages/python_hosts - make a backup of the original to be safe. Also you will need to do this again if you ever update python_hosts

The text changed is:
```                 if line.entry_type == 'ipv4':
                        hosts_file.write(
                            "{0} {1}\n".format(
                                line.address,
                                ' '.join(line.names),
                            )
                        )
                        ipv4_entries_written += 1
                    if line.entry_type == 'ipv6':
                        hosts_file.write(
                            "{0} {1}\n".format(
                                line.address,
                                ' '.join(line.names), ))
                        ipv6_entries_written += 1
```
=====



Finally, ensure you have selected "Reverse DNS lookup" for "Top Clients" within Settings on the PiHole Server 


