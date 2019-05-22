import regex as re
import csv

# Import tools
import tools.helper as helper
from tools.logger import get_logger
from tools.const import ACCESS_RULE_FILENAME, ACCESS_RULE_REGEX, FILE_FORMAT


def generate_access_rules_csv(content, csv_dir, file_format):
    """Process the configuration file and create the access_rules.csv file.

    The method would extract all the access rule lines in the provided config
    file. Every access rule line would be save as AccessRule object for further
    extraction. After further extraction every AccessRule object would be saved
    in the access_rule.csv.

    Args:
        content: Data as string coming from the configuration file.
        csv_dir: Directory where the access_rule.csv would be saved.
        file_format: access rule file can be saved as .csv or .ssv.

    Returns:
        None

    """
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

    with open(cwd, mode="w+") as parsed_config:
        config_writer = csv.writer(
            parsed_config, delimiter=FILE_FORMAT.get(file_format, ",")
        )
        # Write headers

        config_writer.writerow(
            [
                "from",
                "to",
                "action",
                "source address",
                "service",
                "destination address",
                "comment",
            ]
        )

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
                rule.comment,
            ]

            logger.debug("Adding row {}. Contains {}.".format(row_count, rule_content))

            config_writer.writerow(rule_content)
            row_count += 1

    logger.info("Generating Access Rule CSV completed.")


class AccessRule:
    """Extracted access rule line would be further processed in this class.

    Columns that should be displayed in the access_rule.csv would be extracted
    using regular expressions and would be saved in the class attributes.

    Attributes:
        access_rule: The access_rule line to be processed.
        logger: use for logging purposes
        rule_from: e.g. WAN
        rule_to: e.g. LAN
        action: e.g. allow
        src_addr: e.g. Sys_Loggers
        service: e.g. HTTP_HTTPS
        dest_addr: e.g. VPN Conc Group
        comment: e.g. IPv4:From Any to Any for Any service

    """

    def __init__(self, rule, logger):
        """Initialize columns."""
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
        """Populate fields by extracting the needed data using regex."""
        self.rule_from = helper.extract_field_name(
            self._access_rule, r"(?<=\sfrom\s)", flag=re.MULTILINE
        )
        self.rule_to = helper.extract_field_name(
            self._access_rule, r"(?<=\sto\s)")
        self.action = helper.extract_field_name(
            self._access_rule, r"(?<=\saction\s)")
        self.src_addr = helper.extract_column_with_type(
            self._access_rule, r"(?<=\ssource\saddress).+"
        )
        self.service = helper.extract_column_with_type(
            self._access_rule, r"(?<=\sservice\s).+"
        )
        self.dest_addr = helper.extract_column_with_type(
            self._access_rule, r"(?<=\sdestination\saddress\s).+"
        )
        self.comment = helper.extract_field_name(
            self._access_rule, r"(?<=\scomment\s)")

        self._logger.debug(
            "Parsed value: {}".format(
                [
                    self.rule_from,
                    self.rule_to,
                    self.action,
                    self.src_addr,
                    self.service,
                    self.dest_addr,
                    self.comment,
                ]
            )
        )

