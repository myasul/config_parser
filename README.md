# FIREWALL CONFIGURATION PARSER
__Description:__

This script parses a firewall configuration text file and creates multiple CSVs that contains that the parsed data.

__Pre-requisites:__
* Install Python 3. http://docs.python-guide.org/en/latest/starting/installation/
* Install script dependencies. Please run the command below to install all dependencies:
  `pip install --user -r requirements.txt`

__Steps To Use:__
1. There are 6 scripts needed to be able to run the script:
   * config_parser.py
   * parsers/address.py
   * parsers/access_rules.py
   * parsers/address_group.py
   * parsers/services.py
   * parsers/service_group.py
2. Make the config_parser.py executable by running the command below:
   `sudo chmod +x config_parser.py`
3. Place the firewall config file in the same level as the config_parser.py. Run the command below:
   `./config_parser.py <firewall config file>` e.g. `./config_parser.py SonicWall-config.txt`
4. 5 CSV files would be generated inside parsed_csvs directory:
   *  parsed_csvs/access-rules.csv
   *  address.csv
   *  address-grp.csv
   *  services.csv
   *  service-group.csv