import regex as re
import csv

# Import tools
import tools.helper as helper
from tools.logger import get_logger
from tools.const import ADDRESS_REGEX, ADDRESS_FILENAME, \
    FILE_FORMAT, ADDRESS_MULTILINE_REGEX


def generate_address_csv(content, csv_dir, file_format):
    logger = get_logger(__name__)
    logger.info("Generating Address CSV file.")

    # Address has a special case where it can be within one line
    # or span between multiple lines. This is handled by two regexes
    # and stored in a set to avoid duplication.
    addresses = set()
    addresses.update(ADDRESS_REGEX.findall(content))
    addresses.update(ADDRESS_MULTILINE_REGEX.findall(content))
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
            'ip_type', 'ip', 'network_host', 'subnet'])

        # Write address entries
        row_count = 0
        for addr in address_obj:
            if addr.host:
                config_writer.writerow([
                    addr.ip_type,
                    addr.ip,
                    addr.host,
                    '', ])
            elif addr.network:
                config_writer.writerow([
                    addr.ip_type,
                    addr.ip,
                    addr.network,
                    addr.subnet, ])
            else:
                config_writer.writerow([
                    addr.ip_type,
                    addr.ip,
                    '',
                    ''])

            logger.debug("Adding row {}. Contains {}.".format(
                row_count, [
                    addr.ip_type,
                    addr.ip,
                    addr.host,
                    addr.network,
                    addr.subnet
                ]
            ))
            row_count += 1

        logger.info("Generating Address CSV completed.")


class Address:
    def __init__(self, address, logger):
        self._address = address
        self._logger = logger
        self.ip_type = ""
        self.ip = ""
        self.host = ""
        self.network = ""
        self.subnet = ""
        self.populate_fields()

    # Populate fields by extracting the needed data
    # using regular expressions.
    def populate_fields(self):
        self.ip = self._extract_ip()
        self.host = helper.extract_field_name(
            self._address,
            r'(?<=\shost\s)')
        if not self.host:
            self._extract_network_details()

        self._logger.debug("Parsed value: {}".format([
            self.ip,
            self.host,
            self.network,
            self.subnet]))

    def _extract_ip(self):
        self.ip_type = self._extract_ip_type()
        if self.ip_type:
            if self.ip_type == "ipv4":
                return helper.extract_field_name(
                    self._address,
                    pattern=r'(?<=\shost\s)',
                    flag=re.MULTILINE)
            elif self.ip_type == "fqdn":
                return helper.extract_field_name(
                    self._address,
                    pattern=r'(?<=\sdomain\s)',
                    flag=re.MULTILINE)
            elif self.ip_type == "mac":
                return helper.extract_field_name(
                    self._address,
                    pattern=r'(?<=\saddress\s)',
                    flag=re.MULTILINE)

            else:
                return ""
        else:
            return ""

    def _extract_ip_type(self):
        ip_type_match = re.search(
            r'(?:\sipv4\s)|(?:\sipv6\s)|(?:\sfqdn\s)|(?:\smac\s)',
            self._address)
        if ip_type_match:
            ip_type = ip_type_match.group().strip()
            if ip_type in ['ipv4', 'ipv6', 'fqdn', 'mac']:
                return ip_type
            else:
                return ""
        else:
            return ""

    def _extract_network_details(self):
        network_match = re.search(r'(?<=\snetwork\s)' +
                                  r'(?P<network>[^\s]+)\s+(?P<subnet>[^\s]+)',
                                  self._address, re.I)
        if network_match:
            network_details = network_match.groupdict()

            self.network = helper.remove_wrapping_quotes(
                network_details.get('network'))
            self.subnet = helper.remove_wrapping_quotes(
                network_details.get('subnet'))
