import regex as re
import csv
import tools.helper as helper
from tools.const import ADDRESS_GRP_REGEX, ADDRESS_GRP_FILENAME, FILE_FORMAT


def generate_address_grp_csv(content, csv_dir, file_format):
    address_grps = ADDRESS_GRP_REGEX.findall(content)
    address_grp_obj = []
    for addr in address_grps:
        # Create a list of Address objects
        address_grp_obj.append(AddressGroup(addr))

    cwd = csv_dir + "/" + ADDRESS_GRP_FILENAME

    with open(cwd, mode='w+') as parsed_config:
        config_writer = csv.writer(
            parsed_config, delimiter=FILE_FORMAT.get(file_format, ','))
        # Write headers
        config_writer.writerow(['name', 'members'])

        # Write address entries
        for grp in address_grp_obj:
            config_writer.writerow([
                grp.get_ipv4(),
                grp.get_addresses()])


class AddressGroup:
    def __init__(self, address_grp):
        self._address_grp = address_grp
        self._ipv4 = ""
        self._addresses = ""
        self.populate_fields()

    def populate_fields(self):
        self._ipv4 = helper.extract_field_name(
            self._address_grp, r'(?<=address-group\sipv4\s)')
        self._addresses = self._extract_addresses()

    def _extract_addresses(self):
        matches = re.findall(r'(?<=address-object\sipv4).+(?=\n)',
                             self._address_grp, re.I | re.M)
        addresses = [helper.remove_wrapping_quotes(
            match.strip()) for match in matches]

        return ','.join(addresses)

    def get_ipv4(self):
        return self._ipv4

    def get_addresses(self):
        return self._addresses
