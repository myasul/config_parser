import regex as re
import csv

# Import tools
import tools.helper as helper
from tools.logger import get_logger
from tools.const import ADDRESS_GRP_REGEX, ADDRESS_GRP_FILENAME, FILE_FORMAT


def generate_address_grp_csv(content, csv_dir, file_format):
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
    def __init__(self, address_grp, logger):
        self._address_grp = address_grp
        self._logger = logger
        self.ip = ""
        self.addresses = ""
        self.populate_fields()

    # Populate fields by extracting the needed data
    # using regular expressions.
    def populate_fields(self):
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
            self._address_grp, r'(?<=^address-group\s(ipv4|ipv6)\s)')
        return "{};".format(ip)
