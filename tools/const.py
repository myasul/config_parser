import regex as re

ACCESS_RULE_FILENAME = 'access-rules.csv'
ADDRESS_GRP_FILENAME = 'address-grp.csv'
ADDRESS_FILENAME = 'address.csv'
SERVICE_GRP_FILENAME = 'service-group.csv'
SERVICE_FILENAME = 'services.csv'

SERVICE_REGEX = re.compile(r'^service-object.+$', re.I | re.M)
SERVICE_GRP_REGEX = re.compile(r'^service-group.+?exit$', re.I | re.M | re.S)
ADDRESS_REGEX = re.compile(r'^address-object.+$', re.I | re.M)
ACCESS_RULE_REGEX = re.compile(r'^access-rule.+?(?=exit)', re.I | re.M | re.S)
ADDRESS_GRP_REGEX = re.compile(r'^address-group.+?exit$', re.I | re.M | re.S)

FILE_FORMAT = {
    'csv': ',',
    'ssv': ';'
}
