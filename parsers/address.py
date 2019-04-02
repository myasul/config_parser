import re
import csv

ADDRESS_FILENAME = 'address.csv'
ADDRESS_REGEX = re.compile(r'^address-object.+$', re.I | re.M)


def generate_address_csv(content):
    addresses = ADDRESS_REGEX.findall(content)
    address_obj = []
    for addr in addresses:
        # Create a list of Address objects
        address_obj.append(Address(addr))

    with open(ADDRESS_FILENAME, mode='w+') as parsed_config:
        config_writer = csv.writer(parsed_config, delimiter=',')
        # Write headers
        config_writer.writerow([
            'ipv4', 'host', 'network', 'zone'])

        # Write address entries
        for addr in address_obj:
            config_writer.writerow([
                addr.get_ipv4(),
                addr.get_host(),
                addr.get_network(),
                addr.get_zone()])


class Address:
    def __init__(self, address):
        self.address = address
        self.ipv4 = ""
        self.host = ""
        self.network = ""
        self.zone = ""

    def get_ipv4(self):
        match = re.search(r'(?<=address-object\sipv4).+(?=host|network)',
                          self.address, re.I)
        if match:
            self.ipv4 = match.group().strip()

        return self.ipv4

    def get_host(self):
        match = re.search(r'(?<=host\s).+(?=zone)',
                          self.address, re.I)
        if match:
            self.host = match.group().strip()

        return self.host

    def get_network(self):
        match = re.search(r'(?<=network\s).+(?=zone)',
                          self.address, re.I)
        if match:
            self.network = match.group().strip()

        return self.network

    def get_zone(self):
        match = re.search(r'(?<=zone\s).+(?=$)',
                          self.address, re.I)
        if match:
            self.network = match.group().strip()

        return self.network
