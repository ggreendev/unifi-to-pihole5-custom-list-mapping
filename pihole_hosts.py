# -*- coding: utf-8 -*-
""" This module contains classes:
PiHoleHosts:
A extension of python_hosts.Hosts to write file in the format compatible with
the PiHole custom.list file. Each entry being represented as an instance
of the python_hosts.HostsEntry class.
"""

import sys

try:
    from urllib.request import urlopen
except ImportError:  # pragma: no cover
    from urllib2 import urlopen
from python_hosts.utils import (is_ipv4, is_ipv6, is_readable, valid_hostnames,
                                dedupe_list)
from python_hosts import Hosts, HostsEntry
from python_hosts.exception import (InvalidIPv6Address, InvalidIPv4Address,
                                    UnableToWriteHosts)




class PiHoleHosts(Hosts):

    def write(self, path=None):
        """
        Write all of the HostsEntry instances back to the hosts file
        Uses spaces between values instead of tabs the parent class uses.
        :param path: override the write path
        :return: Dictionary containing counts
        """
        written_count = 0
        comments_written = 0
        blanks_written = 0
        ipv4_entries_written = 0
        ipv6_entries_written = 0
        if path:
            output_file_path = path
        else:
            output_file_path = self.hosts_path
        try:
            with open(output_file_path, 'w') as hosts_file:
                for written_count, line in enumerate(self.entries):
                    if line.entry_type == 'comment':
                        hosts_file.write(line.comment + "\n")
                        comments_written += 1
                    if line.entry_type == 'blank':
                        hosts_file.write("\n")
                        blanks_written += 1
                    if line.entry_type == 'ipv4':
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
        except:
            raise UnableToWriteHosts()
        return {'total_written': written_count + 1,
                'comments_written': comments_written,
                'blanks_written': blanks_written,
                'ipv4_entries_written': ipv4_entries_written,
                'ipv6_entries_written': ipv6_entries_written}
