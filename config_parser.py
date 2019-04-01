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
        access_rules_obj.append(AccessRule(rule))

    with open(PARSED_CONFIG_FILENAME, mode='w+') as parsed_config:
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
        self.access_rule = rule
        self.rule_from = ""
        self.rule_to = ""
        self.action = ""
        self.src_addr = ""
        self.service = ""

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

    def get_action(self):
        match = re.search(r'(?<=action).+?(?=\s)',
                          self.access_rule, re.I)
        if match:
            self.action = match.group().strip()

        return self.action

    def get_source_address(self):
        match = re.search(r'(?<=source\saddress).+?(?=service)',
                          self.access_rule, re.I)
        if match:
            self.src_addr = self.get_type(match.group().strip())
        return self.src_addr

    def get_service(self):
        match = re.search(r'(?<=service).+?(?=destination)',
                          self.access_rule, re.I)
        if match:
            self.service = self.get_type(match.group().strip())
        return self.service

    def get_destination_address(self):
        match = re.search(r'(?<=destination\saddress).+?(?=$)',
                          self.access_rule, re.I)
        if match:
            self.service = self.get_type(match.group().strip())
        return self.service

    def get_type(self, data):
        if 'any' in data:
            return 'any'
        elif 'name' in data:
            name_match = re.search(r'(?<=name).+', data, re.I)
            if name_match:
                return name_match.group().strip()
        elif 'group' in data:
            group_match = re.search(r'(?<=group).+', data, re.I)
            if group_match:
                return group_match.group().strip()
        elif data is not None:
            return data.strip()
        return ""


if __name__ == "__main__":
    process_access_rules()
