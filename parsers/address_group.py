import regex as re
import csv
from tools.helper import remove_wrapping_quotes

ADDRESS_GRP_FILENAME = 'address-grp.csv'
ADDRESS_GRP_REGEX = re.compile(r'^address-group.+?exit$', re.I | re.M | re.S)


def generate_address_grp_csv(content, csv_dir):
    address_grps = ADDRESS_GRP_REGEX.findall(content)
    address_grp_obj = []
    for addr in address_grps:
        # Create a list of Address objects
        address_grp_obj.append(AddressGroup(addr))

    cwd = csv_dir + "/" + ADDRESS_GRP_FILENAME

    with open(cwd, mode='w+') as parsed_config:
        config_writer = csv.writer(parsed_config, delimiter=',')
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
        self._extract_ipv4()
        self._extract_addresses()

    def _extract_ipv4(self):
        match = re.search(r'(?<=address-group\sipv4).+(?=\n)',
                          self._address_grp, re.I)
        if match:
            # remove wrapping quotes
            self._ipv4 = "{};".format(remove_wrapping_quotes(match.group()))

    def _extract_addresses(self):
        matches = re.findall(r'(?<=address-object\sipv4).+(?=\n)',
                             self._address_grp, re.I | re.M)
        addresses = [remove_wrapping_quotes(
            match.strip()) for match in matches]

        self._addresses = ','.join(addresses)

    def get_ipv4(self):
        return self._ipv4

    def get_addresses(self):
        return self._addresses
