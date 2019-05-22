import regex as re
import csv

# Import tools
import tools.helper as helper
from tools.logger import get_logger
from tools.const import ADDRESS_GRP_REGEX, ADDRESS_GRP_FILENAME, FILE_FORMAT


def generate_address_grp_csv(content, csv_dir, file_format):
    """Process the configuration file and create the address_grp.csv file.

    The method would extract all the address group lines in the provided config
    file. Every address group line would be save as AddressGroup object for
    further extraction. After further extraction every AddressGroup object
    would be saved in the address_grp.csv.

    Args:
        content: Data as string coming from the configuration file.
        csv_dir: Directory where the address_grp.csv would be saved.
        file_format: address file can be saved as .csv or .ssv.

    Returns:
        None

    """
    logger = get_logger(__name__)
    logger.info("Generating Address Group CSV file.")

    address_grps = ADDRESS_GRP_REGEX.findall(content)
    address_grp_obj = []

    parse_count = 0
    for addr in address_grps:
        # Create a list of Address objects
        logger.debug("Parsing row {}: {}".format(parse_count, addr))
        address_grp_obj.append(AddressGroup(addr, logger))
        logger.debug("Parsing row {} complete.".format(parse_count))

        parse_count += 1

    cwd = csv_dir + "/" + ADDRESS_GRP_FILENAME

    with open(cwd, mode='w+') as parsed_config:
        config_writer = csv.writer(
            parsed_config, delimiter=FILE_FORMAT.get(file_format, ','))
        # Write headers
        config_writer.writerow(['name', 'members'])

        # Write address entries
        row_count = 1
        for grp in address_grp_obj:
            grp_content = [
                grp.ip,
                grp.addresses]

            logger.debug("Adding row {}. Contains {}".format(
                row_count, grp_content))

            config_writer.writerow(grp_content)
            row_count += 1

    logger.info("Generating Address Group CSV completed.")


class AddressGroup:
    """Extracted address_grp line would be further processed in this class.

    Columns that should be displayed in the address_grp.csv would be extracted
    using regular expressions and would be saved in the class attributes.

    Attributes:
        address_grp: The address_grp line to be processed.
        logger: use for logging purposes
        ip: e.g. BadHosts4119
        addresses: list of addresses that are comma separated.
            e.g. TidalFTP,SFTPServ,TidalFTP2

    """

    def __init__(self, address_grp, logger):
        """Initialize columns."""
        self._address_grp = address_grp
        self._logger = logger
        self.ip = ""
        self.addresses = ""
        self.populate_fields()

    def populate_fields(self):
        """Populate fields by extracting the needed data using regex."""
        self.ip = self._extract_ip()
        self.addresses = self._extract_addresses()

        self._logger.debug("Parsed value: {}".format([
            self.ip,
            self.addresses]))

    def _extract_addresses(self):
        matches = re.findall(r'(?<=\s+address-(?:object|group)' +
                             r'\s(?:ipv4|ipv6)).+(?=\n)',
                             self._address_grp, re.I | re.M)
        addresses = [helper.remove_wrapping_quotes(
            match.strip()) for match in matches]

        return ','.join(addresses)

    def _extract_ip(self):
        ip = helper.extract_field_name(
            self._address_grp, r'(?<=^address-group\s(ipv4|ipv6|fqdn|mac)\s)')
        return "{};".format(ip)
