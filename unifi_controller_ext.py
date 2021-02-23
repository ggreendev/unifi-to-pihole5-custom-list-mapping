"""
Extension tp pyunifi.controller to get the network configurations
and from that be able to associate the domain name with network id
"""
from pyunifi.controller import Controller

class ControllerExt(Controller):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)

    def get_network_confs(self):
        """
        Get all Network Configurations
        :return: List of Network Configurations
        """
        return self._api_read('rest/networkconf')

    def get_network_domains(self):
        """
        Gets a dictionary with network ids as keys and
        domain name as value.
        :return: Dictionary of network id and domain
        """
        domains = dict()
        network_confs = self.get_network_confs()
        for conf in network_confs:
            network_id = conf.get("_id")
            domain_name = conf.get("domain_name")
            domains[network_id] = domain_name
        return domains
