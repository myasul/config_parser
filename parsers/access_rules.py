import regex as re
import csv
import tools.helper as helper

ACCESS_RULE_FILENAME = 'access-rules.csv'
ACCESS_RULE_REGEX = re.compile(r'^access-rule.+$', re.I | re.M)


def generate_access_rules_csv(content, csv_dir):
    access_rules = ACCESS_RULE_REGEX.findall(content)
    access_rules_obj = []
    for rule in access_rules:
        # Create a list of AccessRule objects
        access_rules_obj.append(AccessRule(rule))

    cwd = csv_dir + "/" + ACCESS_RULE_FILENAME

    with open(cwd, mode='w+') as parsed_config:
        config_writer = csv.writer(parsed_config, delimiter=',')
        # Write headers
        config_writer.writerow([
            'from', 'to', 'action',
            'source address', 'service', 'destination address'])

        # Write access rule entries
        for rule in access_rules_obj:
            config_writer.writerow([
                rule.get_from(),
                rule.get_to(),
                rule.get_action(),
                rule.get_source_address(),
                rule.get_service(),
                rule.get_destination_address()])


class AccessRule:
    def __init__(self, rule):
        self._access_rule = rule
        self._rule_from = ""
        self._rule_to = ""
        self._action = ""
        self._src_addr = ""
        self._service = ""
        self._dest_addr = ""
        self.populate_fields()

    def populate_fields(self):
        self._rule_from = helper.extract_field_name(
            self._access_rule, r'(?<=access-rule\sfrom).+(?=\sto)')
        self._rule_to = helper.extract_field_name(
            self._access_rule, r'(?<=\sto\s).+?(?=\s)')
        self._action = helper.extract_field_name(
            self._access_rule, r'(?<=action).+?(?=\s)')
        self._src_addr = self._get_type(r'(?<=source\saddress).+')
        self._service = self._get_type(r'(?<=service).+?(?=destination)')
        self._dest_addr = self._get_type(r'(?<=destination\saddress).+?(?=$)')

    def _get_type(self, pattern):
        match = re.search(pattern, self._access_rule)
        if match:
            field = match.group().strip()
            if re.search(r'^any', field):
                return 'any'
            elif re.search(r'^name', field):
                pattern = r'(?<=name\s)((""[^"]+"")|([^\s]+))'
                return helper.extract_field_name(field, pattern)
            elif re.search(r'^group', field):
                pattern = r'(?<=group\s)((""[^"]+"")|([^\s]+))'
                return helper.extract_field_name(field, pattern)
            elif field is not None:
                return field.strip()
        return ""

    def get_from(self):
        return self._rule_from

    def get_to(self):
        return self._rule_to

    def get_action(self):
        return self._action

    def get_source_address(self):
        return self._src_addr

    def get_service(self):
        return self._service

    def get_destination_address(self):
        return self._dest_addr
