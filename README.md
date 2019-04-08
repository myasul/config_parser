# FIREWALL CONFIGURATION PARSER
__Description:__

This script parses a firewall configuration text file and creates multiple CSVs that contains that the parsed data.

__Pre-requisites:__
* Install Python 3. http://docs.python-guide.org/en/latest/starting/installation/
* Install script dependencies. Please run the command below to install all dependencies:
  `pip install --user -r requirements.txt`
* The script can only be run in a Linux flavored machine.
* Make the config_parser.py executable by running the command below:
   `sudo chmod +x config_parser.py`

__Things To Note:__
1. There are several scripts needed to be able to run the script:
   These files should not be moved or altered in any way.
   * config_parser.py
   * parsers/address.py
   * parsers/access_rules.py
   * parsers/address_group.py
   * parsers/services.py
   * parsers/service_group.py
   * tools/const.py
   * tools/helper.py
2. You can also view the detailed description by running:
   `./config_parser.py -h`

__Steps To Use:__
1. Place the firewall config file in the same level as the config_parser.py. Run the command below:
   `./config_parser.py <firewall config file>` e.g. `./config_parser.py SonicWall-config.txt`

   Note: You can also provide the full path if you prefer not to move the file. e.g.:
   `./config_parser.py /home/user/Document/configuration_files/SonicWall-config.txt`

2. You can specify the delimiter that would be used. Currently it supports comma (,) and semicolon (;).
   Just run the script with the `-f` paramenter. Specify either `csv` to use comma as delimiter or `ssv` or to use semicolon. e.g.:
   `./config_parser.py SonicWall-config.txt -f ssv`

3. 5 CSV files would be generated inside parsed_csvs directory:
   *  parsed_csvs/access-rules.csv
   *  address.csv
   *  address-grp.csv
   *  services.csv
   *  service-group.csv

