import regex as re
import csv

# Import tools
import tools.helper as helper
from tools.logger import get_logger
from tools.const import ADDRESS_REGEX, ADDRESS_FILENAME, FILE_FORMAT


def generate_address_csv(content, csv_dir, file_format):
    logger = get_logger(__name__)
    logger.info("Generating Address CSV file.")

    addresses = ADDRESS_REGEX.findall(content)
    address_obj = []

    parse_count = 0
    for addr in addresses:
        # Create a list of Address objects
        logger.debug("Parsing row {}: {}".format(parse_count, addr))
        address_obj.append(Address(addr, logger))
        logger.debug("Parsing row {} complete.".format(parse_count))

        parse_count += 1

    cwd = csv_dir + "/" + ADDRESS_FILENAME

    with open(cwd, mode='w+') as parsed_config:
        config_writer = csv.writer(
            parsed_config, delimiter=FILE_FORMAT.get(file_format, ','))
        # Write headers
        config_writer.writerow([
            'ip', 'network_host', 'subnet'])

        # Write address entries
        row_count = 0
        for addr in address_obj:
            if addr.get_host():
                config_writer.writerow([
                    addr.get_ip(),
                    addr.get_host(),
                    '', ])
            elif addr.get_network():
                config_writer.writerow([
                    addr.get_ip(),
                    addr.get_network(),
                    addr.get_subnet(), ])
            else:
                config_writer.writerow([
                    addr.get_ip(),
                    '',
                    ''])

            logger.debug("Adding row {}. Contains {}.".format(
                row_count, [
                    addr.get_ip(),
                    addr.get_host(),
                    addr.get_network(),
                    addr.get_subnet()
                ]
            ))

        logger.info("Generating Address CSV completed.")


class Address:
    def __init__(self, address, logger):
        self._address = address
        self._ip = ""
        self._host = ""
        self._network = ""
        self._subnet = ""
        self._logger = logger
        self.populate_fields()

    # Populate fields by extracting the needed data
    # using regular expressions.
    def populate_fields(self):
        self._ip = helper.extract_field_name(
            self._address,
            r'(?<=\s(ipv4|ipv6)\s)')
        self._host = helper.extract_field_name(
            self._address,
            r'(?<=\shost\s)')
        if not self._host:
            self._extract_network_details()

        self._logger.debug("Parsed value: {}".format([
            self.get_ip(),
            self.get_host(),
            self.get_network(),
            self.get_subnet()]))

    def _extract_network_details(self):
        network_match = re.search(r'(?<=\snetwork\s)' +
                                  r'(?P<network>[^\s]+)\s+(?P<subnet>[^\s]+)',
                                  self._address, re.I)
        if network_match:
            network_details = network_match.groupdict()

            self._network = helper.remove_wrapping_quotes(
                network_details.get('network'))
            self._subnet = helper.remove_wrapping_quotes(
                network_details.get('subnet'))

    def get_ip(self):
        return self._ip

    def get_host(self):
        return self._host

    def get_network(self):
        return self._network

    def get_subnet(self):
        return self._subnet
