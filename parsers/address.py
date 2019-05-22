import regex as re
import csv
from itertools import chain

# Internal imports
import tools.helper as helper
from tools.logger import get_logger
from tools.const import ADDRESS_REGEX, ADDRESS_FILENAME, \
    FILE_FORMAT, ADDRESS_MULTILINE_REGEX


def generate_address_csv(content, csv_dir, file_format):
    """Process the configuration file and create the address.csv file.

    The method would extract all the address lines in the provided config
    file. Every address line would be save as Address object for further
    extraction. After further extraction every Address object would be saved
    in the address.csv.

    Args:
        content: Data as string coming from the configuration file.
        csv_dir: Directory where the address.csv would be saved.
        file_format: address file can be saved as .csv or .ssv.

    Returns:
        None

    """
    logger = get_logger(__name__)
    logger.info('Generating Address CSV file.')

    # Address has a special case where it can be within one line
    # or span between multiple lines. This is handled by two regexes
    # and stored in a set to avoid duplication.
    addresses1 = {entry for entry in ADDRESS_REGEX.findall(content)}
    addresses2 = {entry for entry in ADDRESS_MULTILINE_REGEX.findall(content)}
    addresses = chain(addresses1, addresses2)

    address_obj = []

    parse_count = 0
    for addr in addresses:
        # Create a list of Address objects
        logger.debug('Parsing row {}: {}'.format(parse_count, addr))
        address_obj.append(Address(addr, logger))
        logger.debug('Parsing row {} complete.'.format(parse_count))

        parse_count += 1

    cwd = csv_dir + '/' + ADDRESS_FILENAME

    with open(cwd, mode='w+') as parsed_config:
        config_writer = csv.writer(
            parsed_config, delimiter=FILE_FORMAT.get(file_format, ','))
        # Write headers
        config_writer.writerow(['ip_type', 'ip',
                                'network_host', 'subnet',
                                'ranges'])

        # Write address entries
        row_count = 0
        for addr in address_obj:
            addr_content = [
                addr.name,
                addr.ip,
                addr.host if addr.host else addr.network,
                addr.subnet,
                addr.range
            ]

            config_writer.writerow(addr_content)

            logger.debug('Adding row {}. Contains {}.'.format(
                row_count, addr_content))
            row_count += 1

        logger.info('Generating Address CSV completed.')


class Address:
    """Extracted address line would be further processed in this class.

    Columns that should be displayed in the address.csv would be extracted
    using regular expressions and would be saved in the class attributes.

    Attributes:
        address: The address line to be processed.
        logger: use for logging purposes
        name: e.g. BadHosts4119
        ip: e.g. 10.202.11.7
        host: e.g. 75.119.211.139
        network: e.g. 10.215.224.0
        subnet: e.g. 255.255.255.240
        range: e.g. 209.46.117.161-209.46.117.191

    """

    def __init__(self, address, logger):
        """Initialize columns."""
        self._address = address
        self._logger = logger
        self.name = ''
        self.ip = ''
        self.host = ''
        self.network = ''
        self.subnet = ''
        self.range = ''
        self.populate_fields()

    def populate_fields(self):
        """Populate fields by extracting the needed data using regex."""
        self.name = self._extract_name()

        # Populate either host, network or range
        # as only one is provided per address-object
        self.host = helper.extract_field_name(
            self._address,
            r'(?<=\shost\s)')
        if self.host:
            self.subnet = '255.255.255.255'
        else:
            self.network, self.subnet = self._extract_network_details()
            if not self.network:
                range_match = re.search(
                    r"\srange\s(?P<range1>[\d.]+)\s(?P<range2>[\d.]+)",
                    self._address)
                if range_match:
                    ranges = range_match.groupdict()
                    self.range = "{}-{}".format(
                        ranges.get('range1'),
                        ranges.get('range2'))

        self.ip = self._extract_ip()

        self._logger.debug('Parsed value: {}'.format([
            self.name,
            self.ip,
            self.host,
            self.network,
            self.subnet,
            self.range]))

    def _extract_ip(self):
        """Extracts IP depending on the protocol/IP type provided"""
        ip_type = self._extract_ip_type()

        if ip_type == 'ipv4':
            return self.host if self.host else self.network
        elif ip_type == 'fqdn':
            return helper.extract_field_name(
                self._address,
                pattern=r'(?<=\sdomain\s)',
                flag=re.MULTILINE)
        elif ip_type == 'mac':
            return helper.extract_field_name(
                self._address,
                pattern=r'(?<=\saddress\s)',
                flag=re.MULTILINE)
        else:
            return ''

    def _extract_ip_type(self):
        """Extract the IP type that will be used for extracting the IP."""
        ip_type_match = re.search(
            r'(?:\sipv4\s)|(?:\sipv6\s)|(?:\sfqdn\s)|(?:\smac\s)',
            self._address)
        if ip_type_match:
            ip_type = ip_type_match.group().strip()
            if ip_type in ['ipv4', 'ipv6', 'fqdn', 'mac']:
                return ip_type

            else:
                error = 'IP Type of {} is unknown'.format(self._address)
                self._logger.error(error)
                raise ValueError(error)
        else:
            error = 'IP Type of {} is unknown'.format(self._address)
            self._logger.error(error)
            raise ValueError(error)

    def _extract_name(self):
        ip_type = self._extract_ip_type()
        return helper.extract_field_name(
            self._address, r'(?<=\s{}\s)'.format(ip_type))

    def _extract_network_details(self):
        """Extract network which consists of extracting network and subnet."""
        network = subnet = ""
        network_match = re.search(r'(?<=\snetwork\s)' +
                                  r'(?P<network>[^\s]+)\s+(?P<subnet>[^\s]+)',
                                  self._address, re.I)
        if network_match:
            network_details = network_match.groupdict()

            network = helper.remove_wrapping_quotes(
                network_details.get('network'))
            subnet = helper.remove_wrapping_quotes(
                network_details.get('subnet'))

        return network, subnet
