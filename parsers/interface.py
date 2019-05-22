import regex as re
import csv

# Internal imports
import tools.helper as helper
from tools.logger import get_logger
from tools.const import INTERFACE_FILENAME, INTERFACE_REGEX, FILE_FORMAT


def generate_interface_csv(content, csv_dir, file_format):
    """Process the configuration file and create the interface.csv file.

    The method would extract all the interface lines in the provided config
    file. Every interface line would be save as Interface object for further
    extraction. After further extraction every Interface object would be saved
    in the interface.csv.

    Args:
        content: Data as string coming from the configuration file.
        csv_dir: Directory where the interface.csv would be saved.
        file_format: interface file can be saved as .csv or .ssv.

    Returns:
        None

    """
    logger = get_logger(__name__)
    logger.info("Generating Interface CSV file.")

    interfaces = INTERFACE_REGEX.findall(content)
    interfaces_obj = []

    parse_count = 0
    for interface in interfaces:
        # Create a list of Interface objects
        logger.debug("Parsing row {}: {}.".format(parse_count, interface))
        interfaces_obj.append(Interface(interface, logger))
        logger.debug("Parsing row {} complete.".format(parse_count))

    cwd = csv_dir + "/" + INTERFACE_FILENAME

    with open(cwd, mode='w+') as parsed_config:
        config_writer = csv.writer(
            parsed_config, delimiter=FILE_FORMAT.get(file_format, ','))
        # Write headers
        config_writer.writerow([
            'name', 'vlan', 'ip', 'netmask'])

        # Write address entries
        row_count = 1
        for interface in interfaces_obj:
            interface_content = [
                interface.name,
                interface.vlan,
                interface.ip,
                interface.netmask]

            logger.debug("Adding row {}. Contains {}".format(
                row_count, interface_content))

            config_writer.writerow(interface_content)


class Interface:
    """Extracted address line would be further processed in this class.

    Columns that should be displayed in the address.csv would be extracted
    using regular expressions and would be saved in the class attributes.

    Attributes:
        interface: The interface line to be processed.
        logger: use for logging purposes
        name: e.g. BadHosts4119
        ip: e.g. 10.202.11.7
        netmask: e.g. 75.119.211.139
        vlan: e.g. 10.215.224.0

    """

    def __init__(self, interface, logger):
        self._interface = interface
        self._logger = logger
        self.name = ""
        self.ip = ""
        self.netmask = ""
        self.vlan = ""
        self.populate_fields()

    def populate_fields(self):
        """Populate fields by extracting the needed data using regex."""
        self.name = self._extract_interface_name()
        self.ip = helper.extract_field_name(self._interface, r'(?<=\bip\s)')
        self.netmask = helper.extract_field_name(
            self._interface, r'(?<=netmask\s)')
        self.vlan = helper.extract_field_name(
            self._interface, r'(?<=\svlan\s)')

        self._logger.debug("Parsed value: {}".format([
            self.name,
            self.ip,
            self.netmask
        ]))

    def _extract_interface_name(self):
        interface = re.search(
            r'^interface\s(?:ipv6\s)?([^\s]+)', self._interface)
        if interface:
            return helper.remove_wrapping_quotes(interface.group(1))
        return ""
