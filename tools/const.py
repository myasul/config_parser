import regex as re

ACCESS_RULE_FILENAME = 'access-rules.csv'
ADDRESS_GRP_FILENAME = 'address-grp.csv'
ADDRESS_FILENAME = 'address.csv'
SERVICE_GRP_FILENAME = 'service-group.csv'
SERVICE_FILENAME = 'services.csv'
ZONE_FILENAME = 'zones.csv'
INTERFACE_FILENAME = 'interface.csv'
NAT_POLICY_FILENAME = 'nat_policy.csv'

SERVICE_REGEX = re.compile(r'^service-object.+$', re.I | re.M)
SERVICE_GRP_REGEX = re.compile(r'^service-group.+?exit$', re.I | re.M | re.S)
ADDRESS_REGEX = re.compile(r'^address-object.+zone.+$', re.I | re.M)
ADDRESS_MULTILINE_REGEX = re.compile(
    r'(^address-object.+$\n(?:[^\n]+$\n)+\s+exit)', re.I | re.M)
ACCESS_RULE_REGEX = re.compile(r'^access-rule.+?(?=exit)', re.I | re.M | re.S)
ADDRESS_GRP_REGEX = re.compile(r'^address-group.+?exit$', re.I | re.M | re.S)
ZONE_REGEX = re.compile(r'^zone.+?exit$', re.I | re.M | re.S)
INTERFACE_REGEX = re.compile(
    r'^interface.+?(?:^\s{4}exit)$', re.I | re.M | re.S)
NAT_POLICY_REGEX = re.compile(r'^nat-policy.+?exit$', re.I | re.M | re.S)

WINDOWS_LINE_ENDING = b'\r\n'
UNIX_LINE_ENDING = b'\n'

FILE_FORMAT = {
    'csv': ',',
    'ssv': ';'
}
