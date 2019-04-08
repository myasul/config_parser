#!/usr/bin/env python3
"""FIREWALL CONFIGURATION PARSER

This script parses a firewall configuration text file, extracts needed
data, and creates multiple CSVs that contains the parsed data. There will 
be a total of files that will be generated, all contained in the parsed_csv
folder, namely:
* parsed_csv/access-rules.csv
* parsed_csv/address-grp.csv
* parsed_csv/address.csv
* parsed_csv/service-group.csv
* parsed_csv/services.csv

PRE-REQUISITES
* Install Python 3. http://docs.python-guide.org/en/latest/starting/installation/
* Install script dependencies.
Please run the command below to install all dependencies:
pip install --user -r requirements.txt
* The script can only be run in a Linux flavored machine.
* Make the config_parser.py executable by running the command below: 
sudo chmod +x config_parser.py
"""

# TODO :: LIST
# 1. Create logging
# 2. Add meaningful comments
# 3. Check if classes can be more concise. e.g. Add a parent class
# 4. Implement argparser library

import regex as re
import csv
import sys
import os
import argparse
from argparse import RawTextHelpFormatter

# Import config parsers
from parsers.access_rules import generate_access_rules_csv
from parsers.address import generate_address_csv
from parsers.address_group import generate_address_grp_csv
from parsers.services import generate_service_csv
from parsers.service_group import generate_service_grp_csv

# CSV File names
SERVICES_FILENAME = 'services.csv'
SERVICES_GRP_FILENAME = 'services-grp.csv'


# Main method that combines all the parsers and calls
# them one by one to create csv/ssv files.
def process_config_file(file_path, file_format):
    if not file_format:
        print("[ERROR] File format not specified."
              "Run './config_parser.py -h' for detailed instructions.")

    if os.path.exists(file_path):
        # read config file contents
        with open(file_path, 'r') as config_file:
            content = config_file.read()
    else:
        print("[ERROR] {} cannot be found. ".format(file_path) +
              "Please put it beside the config parser script " +
              "or please specify the full valid path.")
        return False

    csv_dir = "{}/parsed_csvs".format(os.getcwd())
    if not os.path.exists(csv_dir):
        os.mkdir(csv_dir)

    generate_access_rules_csv(content, csv_dir, file_format)
    generate_address_csv(content, csv_dir, file_format)
    generate_address_grp_csv(content, csv_dir, file_format)
    generate_service_csv(content, csv_dir, file_format)
    generate_service_grp_csv(content, csv_dir, file_format)
    return True


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=RawTextHelpFormatter
    )
    path_help = 'Path where the configuration is located. ' \
        'You only need to enter the file name if the config file' \
        'and the config_parser.py is in the same location.'
    parser.add_argument(
        'path',
        type=str,
        default='',
        help=path_help)

    format_help = 'The delimiter that will be used ' \
        'for separating values in the file. The script support comma' \
        ' and semicolon to separate columns and values inside the file.'
    parser.add_argument(
        '-f',
        '--format',
        type=str,
        default='csv',
        choices=['csv', 'ssv'],
        help=format_help)

    args = parser.parse_args()

    if not args.path:
        print(
            "[ERROR] Please input filename. e.g. " +
            "'/config_parser --path test_config.txt'")

    success = process_config_file(args.path, args.format)
    if success:
        print(
            "[CONFIRMATION] Config file parsed successfully. " +
            "Please see CSV files.")


if __name__ == "__main__":
    main()
