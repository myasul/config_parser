#!/usr/bin/env python
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
# 1. Create logging - DONE
# 2. Add meaningful comments
# 3. Check if classes can be more concise. e.g. Add a parent class
# 4. Implement argparser library - DONE
# 5. Implement Generator comprehension

# CURRENT LIMITATION
# 1. If the column that is surrounded by spaces appeared more than once, it may
#   retrieve a value different from what is expected

import regex as re
import csv
import sys
import os
import argparse
import logging
from argparse import RawTextHelpFormatter
from tools.logger import get_logger
from tools.const import WINDOWS_LINE_ENDING, UNIX_LINE_ENDING

# Import config parsers
from parsers.access_rules import generate_access_rules_csv
from parsers.address import generate_address_csv
from parsers.address_group import generate_address_grp_csv
from parsers.services import generate_service_csv
from parsers.service_group import generate_service_grp_csv
from parsers.zone import generate_zone_csv
from parsers.interface import generate_interface_csv
from parsers.nat_policy import generate_nat_policy_csv

# CSV File names
SERVICES_FILENAME = 'services.csv'
SERVICES_GRP_FILENAME = 'services-grp.csv'


# Main method that combines all the parsers and calls
# them one by one to create csv/ssv files.
def process_config_file(file_path, file_format):
    logger = get_logger(__name__)

    logger.info("{} si being parsed.".format(file_path))

    if not file_format:
        error_message = "[ERROR] File format not specified. " \
                        "Run './config_parser.py -h'" \
                        "for detailed instructions."
        logger.error(error_message)
        print "[ERROR] {}".format(error_message)

    try:
        # read config file contents
        with open(file_path, 'r') as config_file:
            content = config_file.read()
            content = content.replace(WINDOWS_LINE_ENDING, UNIX_LINE_ENDING)
    except IOError:
        error_message = ("{} cannot be found or {} is a directory."
                         " Please put it beside the config parser script "
                         "or please specify the full valid path.").format(
            file_path, file_path)
        logger.error(error_message)
        print "[ERROR] {}".format(error_message)
        return False

    # Create folder where the parsed csvs would be stored
    csv_dir = "{}/parsed_csvs".format(os.getcwd())
    if not os.path.exists(csv_dir):
        os.mkdir(csv_dir)

    generate_access_rules_csv(content, csv_dir, file_format)
    generate_address_csv(content, csv_dir, file_format)
    generate_address_grp_csv(content, csv_dir, file_format)
    generate_service_csv(content, csv_dir, file_format)
    generate_service_grp_csv(content, csv_dir, file_format)
    generate_zone_csv(content, csv_dir, file_format)
    generate_interface_csv(content, csv_dir, file_format)
    generate_nat_policy_csv(content, csv_dir, file_format)
    return True


def main():
    logger = get_logger(__name__)

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

    # Used for debugging
    # args = argparse.Namespace(
    #     path='test_config_files/test-config-file.txt', format='csv')

    args = parser.parse_args()

    success = process_config_file(args.path, args.format)
    if success:
        message = ("Config file {} parsed successfully. "
                   "Please see CSV files saved in parsed_csvs/ directory."
                   ).format(args.path)
        logger.info(message)
        print "[CONFIRMATION] {}".format(message)


if __name__ == "__main__":
    main()
