import regex as re
import csv

# Import tools
import tools.helper as helper
from tools.logger import get_logger
from tools.const import NAT_POLICY_FILENAME, NAT_POLICY_REGEX, FILE_FORMAT


def generate_nat_policy_csv(content, csv_dir, file_format):
    """Process the configuration file and create the nat_policy.csv file.

    The method would extract all the nat_policy lines in the provided config
    file. Every nat_policy line would be save as NatPolicy object for further
    extraction. After further extraction every NatPolicy object would be saved
    in the nat_policy.csv.

    Args:
        content: Data as string coming from the configuration file.
        csv_dir: Directory where the nat_policy.csv would be saved.
        file_format: nat_policy file can be saved as .csv or .ssv.

    Returns:
        None

    """
    logger = get_logger(__name__)
    logger.info("Generating NAT Policy CSV file.")

    policies = NAT_POLICY_REGEX.findall(content)
    policies_obj = []

    parse_count = 0
    for policy in policies:
        # Create a list of Address objects
        logger.debug("Parsing row {}: {}.".format(parse_count, policy))
        policies_obj.append(NatPolicy(policy, logger))
        logger.debug("Parsing row {} complete.".format(parse_count))

    cwd = csv_dir + "/" + NAT_POLICY_FILENAME

    with open(cwd, mode="w+") as parsed_config:
        config_writer = csv.writer(
            parsed_config, delimiter=FILE_FORMAT.get(file_format, ",")
        )
        # Write headers
        config_writer.writerow(
            [
                "from",
                "to",
                "source",
                "destination",
                "tp-source",
                "tp-destination",
                "service",
            ]
        )

        # Write nat policy entries
        row_count = 1
        for policy in policies_obj:
            policy_content = [
                policy.policy_from,
                policy.policy_to,
                policy.src,
                policy.dest,
                policy.tp_src,
                policy.tp_dest,
                policy.service,
            ]

            logger.debug(
                "Adding row {}. Contains {}.".format(row_count, policy_content)
            )

            config_writer.writerow(policy_content)

    logger.info("Generating Access Rule CSV completed.")


class NatPolicy:
    """Extracted nat_policy line would be further processed in this class.

    Columns that should be displayed in the nat_policy.csv would be extracted
    using regular expressions and would be saved in the class attributes.

    Attributes:
        policy: The nat_policy line to be processed.
        logger: use for logging purposes
        policy_from: e.g. X5:V2325
        policy_to: e.g. X4
        src: e.g. DCWebGW
        dest: e.g. LCAA-NAT
        tp_src: e.g. LCWS-NAT
        tp_dest: e.g. MRP-VIP-DMZ
        service: e.g. HTTPS

    """

    def __init__(self, policy, logger):
        """Initialize columns."""
        self._policy = policy
        self._logger = logger
        self.policy_from = ""
        self.policy_to = ""
        self.src = ""
        self.dest = ""
        self.tp_src = ""
        self.tp_dest = ""
        self.service = ""
        self.populate_fields()

    def populate_fields(self):
        """Populate fields by extracting the needed data using regex."""
        self.policy_from = helper.extract_field_name(
            self._policy, r"(?<=\sinbound\s)")
        self.policy_to = helper.extract_field_name(
            self._policy, r"(?<=\soutbound\s)")
        self.src = helper.extract_column_with_type(
            self._policy, r"(?<=\ssource\s).+")
        self.dest = helper.extract_column_with_type(
            self._policy, r"(?<=\sdestination\s).+")
        self.tp_src = helper.extract_column_with_type(
            self._policy, r"(?<=\stranslated-source\s).+")
        self.tp_dest = helper.extract_column_with_type(
            self._policy, r"(?<=\stranslated-destination\s).+")
        self.service = helper.extract_column_with_type(
            self._policy, r"(?<=\sservice\s).+")
