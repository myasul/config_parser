import regex as re
import csv

ADDRESS_GRP_FILENAME = 'address-grp.csv'
ADDRESS_GRP_REGEX = re.compile(r'^address-group.+?exit$', re.I | re.M | re.S)


def generate_address_grp_csv(content):
    address_grps = ADDRESS_GRP_REGEX.findall(content)
    address_grp_obj = []
    for addr in address_grps:
        # Create a list of Address objects
        address_grp_obj.append(AddressGroup(addr))

    with open(ADDRESS_GRP_FILENAME, mode='w+') as parsed_config:
        config_writer = csv.writer(parsed_config, delimiter=',')
        # Write headers
        config_writer.writerow(['ipv4', 'address'])

        # Write address entries
        for grp in address_grp_obj:
            if len(grp.get_addresses()) > 0:
                for addr in grp.get_addresses():
                    config_writer.writerow([
                        grp.get_ipv4_grp(),
                        addr])
            else:
                config_writer.writerow([
                    grp.get_ipv4_grp(),
                    ""
                ])


class AddressGroup:
    def __init__(self, address_grp):
        self.address_grp = address_grp
        self.ipv4_grp = ""
        self.addresses = []

    def get_ipv4_grp(self):
        match = re.search(r'(?<=address-group\sipv4).+(?=\n)',
                          self.address_grp, re.I)
        if match:
            self.ipv4_grp = match.group().strip()

        return self.ipv4_grp

    def get_addresses(self):
        self.addresses = []
        matches = re.findall(r'(?<=address-object).+(?=\n)',
                             self.address_grp, re.I | re.M)
        for match in matches:
            self.addresses.append(match.strip())

        return self.addresses
