import regex as re
import csv

# Import tools
import tools.helper as helper
from tools.logger import get_logger
from tools.const import ACCESS_RULE_FILENAME, ACCESS_RULE_REGEX, FILE_FORMAT


def generate_access_rules_csv(content, csv_dir, file_format):
    logger = get_logger(__name__)
    logger.info("Generating Access Rules CSV file.")

    access_rules = ACCESS_RULE_REGEX.findall(content)
    access_rules_obj = []

    parse_count = 0
    for rule in access_rules:
        # Create a list of AccessRule objects
        logger.debug("Parsing row {}: {}.".format(parse_count, rule))
        access_rules_obj.append(AccessRule(rule, logger))
        logger.debug("Parsing row {} complete.".format(parse_count))

        parse_count += 1

    cwd = csv_dir + "/" + ACCESS_RULE_FILENAME

    with open(cwd, mode='w+') as parsed_config:
        config_writer = csv.writer(
            parsed_config, delimiter=FILE_FORMAT.get(file_format, ','))
        # Write headers

        config_writer.writerow([
            'from', 'to', 'action',
            'source address', 'service', 'destination address',
            'comment'])

        # Write access rule entries
        row_count = 1
        for rule in access_rules_obj:
            rule_content = [
                rule.rule_from,
                rule.rule_to,
                rule.action,
                rule.src_addr,
                rule.service,
                rule.dest_addr,
                rule.comment]

            logger.debug("Adding row {}. Contains {}.".format(
                row_count, rule_content))

            config_writer.writerow(rule_content)
            row_count += 1

    logger.info("Generating Access Rule CSV completed.")


class AccessRule:
    def __init__(self, rule, logger):
        self._access_rule = rule
        self._logger = logger
        self.rule_from = ""
        self.rule_to = ""
        self.action = ""
        self.src_addr = "any"
        self.service = "any"
        self.dest_addr = "any"
        self.comment = ""
        self.populate_fields()

    # Populate fields by extracting the needed data
    # using regular expressions.
    def populate_fields(self):
        self.rule_from = helper.extract_field_name(
            self._access_rule, r'(?<=\sfrom\s)', flag=re.MULTILINE)
        self.rule_to = helper.extract_field_name(
            self._access_rule, r'(?<=\sto\s)')
        self.action = helper.extract_field_name(
            self._access_rule, r'(?<=\saction\s)')
        self.src_addr = self._get_type(r'(?<=\ssource\saddress).+')
        self.service = self._get_type(r'(?<=\sservice\s).+')
        self.dest_addr = self._get_type(r'(?<=\sdestination\saddress\s).+')
        self.comment = helper.extract_field_name(
            self._access_rule, r'(?<=\scomment\s)')

        self._logger.debug("Parsed value: {}".format([
            self.rule_from,
            self.rule_to,
            self.action,
            self.src_addr,
            self.service,
            self.dest_addr,
            self.comment]))

    def _get_type(self, pattern):
        match = re.search(pattern, self._access_rule)
        if match:
            field = match.group().strip()
            if re.search(r'^any', field):
                return 'any'
            elif re.search(r'^name', field):
                pattern = r'(?<=name\s)'
                return helper.extract_field_name(field, pattern)
            elif re.search(r'^group', field):
                pattern = r'(?<=group\s)'
                return helper.extract_field_name(field, pattern)
            elif field is not None:
                return field.strip()
        return ""
