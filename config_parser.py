#!/usr/bin/env python3
import re
import csv
import sys
import os

# CSV File names
ACCESS_RULE_FILENAME = 'access-rules.csv'
ADDRESS_FILENAME = 'address.csv'
ADDRESS_GRP_FILENAME = 'address-grp.csv'
SERVICES_FILENAME = 'services.csv'
SERVICES_GRP_FILENAME = 'services-grp.csv'

# Regexes
ACCESS_RULE_REGEX = re.compile(r'^access-rule.+$', re.I | re.M)
ADDRESS_REGEX = re.compile(r'^address-object.+$', re.I | re.M)


def generate_address_csv(content):
    addresses = ADDRESS_REGEX.findall(content)
    address_obj = []
    for addr in addresses:
        # Create a list of Address objects
        address_obj.append(Address(addr))

    with open(ADDRESS_FILENAME, mode='w+') as parsed_config:
        config_writer = csv.writer(parsed_config, delimiter=',')
        # Write headers
        config_writer.writerow([
            'ipv4', 'host', 'network', 'zone'])

        # Write address entries
        for addr in address_obj:
            config_writer.writerow([
                addr.get_ipv4(),
                addr.get_host(),
                addr.get_network(),
                addr.get_zone()])


def generate_access_rules_csv(content):
    access_rules = ACCESS_RULE_REGEX.findall(content)
    access_rules_obj = []
    for rule in access_rules:
        # Create a list of AccessRule objects
        access_rules_obj.append(AccessRule(rule))

    with open(ACCESS_RULE_FILENAME, mode='w+') as parsed_config:
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


def process_config_file(file_name):
    if os.path.exists(file_name):
        # read config file contents
        with open(file_name, 'r') as config_file:
            content = config_file.read()
    else:
        print("[ERROR] {} cannot be found. ".format(file_name) +
              "Please put it beside the config parser script " +
              "or please specify the full valid path.")
        return

    generate_access_rules_csv(content)
    generate_address_csv(content)


class Address:
    def __init__(self, address):
        self.address = address
        self.ipv4 = ""
        self.host = ""
        self.network = ""
        self.zone = ""

    def get_ipv4(self):
        match = re.search(r'(?<=address-object\sipv4).+(?=host|network)',
                          self.address, re.I)
        if match:
            self.ipv4 = match.group().strip()

        return self.ipv4

    def get_host(self):
        match = re.search(r'(?<=host\s).+(?=zone)',
                          self.address, re.I)
        if match:
            self.host = match.group().strip()

        return self.host

    def get_network(self):
        match = re.search(r'(?<=network\s).+(?=zone)',
                          self.address, re.I)
        if match:
            self.network = match.group().strip()

        return self.network

    def get_zone(self):
        match = re.search(r'(?<=zone\s).+(?=$)',
                          self.address, re.I)
        if match:
            self.network = match.group().strip()

        return self.network


'''
Access Rule object to extract necessary parts needed to be displayed
in an access rule. This utilizes regular expression that focuses
on lookbehinds and lookaheads
'''


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
    try:
        file_name = sys.argv[1].strip()
        process_config_file(file_name)
        print(
            "[CONFIRMATION] Config file parsed successfully. " +
            "Please see CSV files.")
    except IndexError:
        print(
            "[ERROR] Please input filename. e.g. " +
            "'/config_parser test_config.txt'")
