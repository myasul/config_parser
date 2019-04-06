#!/usr/bin/env python3
"""Firewall Configuration Parser

This script parses a firewall configuration text file and creates
multiple CSVs that contains that the parsed data.
"""

# TODO :: LIST
# 1. Create logging
# 2. Add meaningful comments
# 3. Check if classes can be more concise. e.g. Add a parent class

import regex as re
import csv
import sys
import os

# Import config parsers
from parsers.access_rules import generate_access_rules_csv
from parsers.address import generate_address_csv
from parsers.address_group import generate_address_grp_csv
from parsers.services import generate_service_csv
from parsers.service_group import generate_service_grp_csv

# CSV File names
SERVICES_FILENAME = 'services.csv'
SERVICES_GRP_FILENAME = 'services-grp.csv'


def process_config_file(file_name):
    if os.path.exists(file_name):
        # read config file contents
        with open(file_name, 'r') as config_file:
            content = config_file.read()
    else:
        print("[ERROR] {} cannot be found. ".format(file_name) +
              "Please put it beside the config parser script " +
              "or please specify the full valid path.")
        return False

    csv_dir = "{}/parsed_csvs".format(os.getcwd())
    if not os.path.exists(csv_dir):
        os.mkdir(csv_dir)

    generate_access_rules_csv(content, csv_dir)
    generate_address_csv(content, csv_dir)
    generate_address_grp_csv(content, csv_dir)
    generate_service_csv(content, csv_dir)
    generate_service_grp_csv(content, csv_dir)
    return True


def main():
    try:
        file_name = sys.argv[1].strip()
        success = process_config_file(file_name)
        if success:
            print(
                "[CONFIRMATION] Config file parsed successfully. " +
                "Please see CSV files.")
    except IndexError:
        print(
            "[ERROR] Please input filename. e.g. " +
            "'/config_parser test_config.txt'")


if __name__ == "__main__":
    main()
