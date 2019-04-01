#!/usr/bin/env python3
import re
import csv

CONFIG_FILENAME = 'SonicWall-config.txt'
PARSED_CONFIG_FILENAME = 'SonicWall-parsed.csv'
ACCESS_RULE_REGEX = re.compile(r'^access-rule.+$', re.I | re.M)


def process_access_rules():
    # read config file contents
    with open(CONFIG_FILENAME, 'r') as config_file:
        content = config_file.read()

    access_rules = ACCESS_RULE_REGEX.findall(content)
    access_rules_obj = []
    for rule in access_rules:
        access_rules_obj.append(AccessRules(rule))

    with open(PARSED_CONFIG_FILENAME, mode='w+') as parsed_config:
        config_writer = csv.writer(parsed_config, delimiter=',')
        # Write headers
        config_writer.writerow(['from', 'to'])

        # Write access rule entries
        for rule in access_rules_obj:
            config_writer.writerow([rule.get_from(), rule.get_to()])


class AccessRules:
    def __init__(self, rule):
        self.access_rule = rule
        self.rule_from = ""
        self.rule_to = ""

    def get_from(self):
        match = re.search(r'(?<=access-rule\sfrom).+(?=\sto)',
                          self.access_rule, re.I)
        if match:
            self.rule_from = match.group().strip()

        return self.rule_from

    def get_to(self):
        match = re.search(r'(?<={}\sto).+?(?=\s)'.format(
            self.rule_from),
            self.access_rule, re.I)
        if match:
            self.rule_to = match.group().strip()

        return self.rule_to


if __name__ == "__main__":
    process_access_rules()
