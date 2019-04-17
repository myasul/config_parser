import regex as re
import csv

# Import tools
import tools.helper as helper
from tools.logger import get_logger
from tools.const import INTERFACE_FILENAME, INTERFACE_REGEX, FILE_FORMAT


def generate_interface_csv(content, csv_dir, file_format):
    logger = get_logger(__name__)
    logger.info("Generating Interface CSV file.")

    interfaces = INTERFACE_REGEX.findall(content)
    interfaces_obj = []

    parse_count = 0
    for interface in interfaces:
        print interface
        # Create a list of Address objects
        logger.debug("Parsing row {}: {}.".format(parse_count, interface))
        interfaces_obj.append(Interface(interface, logger))
        logger.debug("Parsing row {} complete.".format(parse_count))

    cwd = csv_dir + "/" + INTERFACE_FILENAME

    with open(cwd, mode='w+') as parsed_config:
        config_writer = csv.writer(
            parsed_config, delimiter=FILE_FORMAT.get(file_format, ','))
        # Write headers
        config_writer.writerow([
            'name', 'ip', 'netmask'])

        # Write address entries
        row_count = 1
        for interface in interfaces_obj:
            interface_content = [
                interface.name,
                interface.ip,
                interface.netmask]

            logger.debug("Adding row {}. Contains {}".format(
                row_count, interface_content))

            config_writer.writerow(interface_content)


class Interface:
    def __init__(self, interface, logger):
        self._interface = interface
        self._logger = logger
        self.name = ""
        self.ip = ""
        self.netmask = ""
        self.populate_fields()

    # Populate fields by extracting the needed data
    # using regular expressions.
    def populate_fields(self):
        self.name = helper.extract_field_name(
            self._interface, r'(?<=interface\s)')
        self.ip = helper.extract_field_name(self._interface, r'(?<=\bip\s)')
        self.netmask = helper.extract_field_name(
            self._interface, r'(?<=netmask\s)')

        self._logger.debug("Parsed value: {}".format([
            self.name,
            self.ip,
            self.netmask
        ]))
