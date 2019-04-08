import regex as re
import csv
import tools.helper as helper
from tools.const import ADDRESS_REGEX, ADDRESS_FILENAME, FILE_FORMAT


def generate_address_csv(content, csv_dir, file_format):
    addresses = ADDRESS_REGEX.findall(content)
    address_obj = []
    for addr in addresses:
        # Create a list of Address objects
        address_obj.append(Address(addr))

    cwd = csv_dir + "/" + ADDRESS_FILENAME

    with open(cwd, mode='w+') as parsed_config:
        config_writer = csv.writer(
            parsed_config, delimiter=FILE_FORMAT.get(file_format, ','))
        # Write headers
        config_writer.writerow([
            'ipv4', 'network_host', 'subnet'])

        # Write address entries
        for addr in address_obj:
            if addr.get_host():
                config_writer.writerow([
                    addr.get_ipv4(),
                    addr.get_host(),
                    '', ])
            elif addr.get_network():
                config_writer.writerow([
                    addr.get_ipv4(),
                    addr.get_network(),
                    addr.get_subnet(), ])
            else:
                config_writer.writerow([
                    addr.get_ipv4(),
                    '',
                    ''])


class Address:
    def __init__(self, address):
        self._address = address
        self._ipv4 = ""
        self._host = ""
        self._network = ""
        self._subnet = ""
        self.populate_fields()

    def populate_fields(self):
        self._ipv4 = helper.extract_field_name(
            self._address,
            r'(?<=ipv4\s)')
        self._host = helper.extract_field_name(
            self._address,
            r'(?<=host\s)')
        if not self._host:
            self._extract_network_details()

    def _extract_network_details(self):
        network_match = re.search(r'(?<=network\s)' +
                                  r'(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})\s+' +
                                  r'(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})',
                                  self._address, re.I)
        if network_match:
            self._network = network_match.group(1)
            self._subnet = network_match.group(2)

    def get_ipv4(self):
        return self._ipv4

    def get_host(self):
        return self._host

    def get_network(self):
        return self._network

    def get_subnet(self):
        return self._subnet
