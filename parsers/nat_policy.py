import regex as re
import csv

# Import tools
import tools.helper as helper
from tools.logger import get_logger
from tools.const import NAT_POLICY_FILENAME, NAT_POLICY_REGEX, FILE_FORMAT


def generate_nat_policy_csv(content, csv_dir, file_format):
    logger = get_logger(__name__)
    logger.info('Generating NAT Policy CSV file.')

    policies = NAT_POLICY_REGEX.findall(content)
    policies_obj = []

    parse_count = 0
    for policy in policies:
        # Create a list of Address objects
        logger.debug('Parsing row {}: {}.'.format(parse_count, policy))
        # policies_obj.append(Policy(policy, logger))
        policies_obj.append(NatPolicy(policy, logger))
        logger.debug('Parsing row {} complete.'.format(parse_count))

    cwd = csv_dir + '/' + NAT_POLICY_FILENAME

    with open(cwd, mode='w+') as parsed_config:
        config_writer = csv.writer(
            parsed_config, delimiter=FILE_FORMAT.get(file_format, ',')
        )
        # Write headers
        config_writer.writerow([
            'from', 'to', 'source', 'destination',
            'tp-source', 'tp-destination', 'service'
        ])

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
                policy.service
            ]

            logger.debug("Adding row {}. Contains {}.".format(
                row_count, policy_content))

            config_writer.writerow(policy_content)

    logger.info("Generating Access Rule CSV completed.")


class NatPolicy:
    def __init__(self, policy, logger):
        self._policy = policy
        self._logger = logger
        self.policy_from = ''
        self.policy_to = ''
        self.src = ''
        self.dest = ''
        self.tp_src = ''
        self.tp_dest = ''
        self.service = ''
        self.populate_fields()

    def populate_fields(self):
        self.policy_from = helper.extract_field_name(
            self._policy, r'(?<=\sinbound\s)')
        self.policy_to = helper.extract_field_name(
            self._policy, r'(?<=\soutbound\s)')
        self.src = self._get_type(r'(?<=\ssource\s).+')
        self.dest = self._get_type(r'(?<=\sdestination\s).+')
        self.tp_src = self._get_type(r'(?<=\stranslated-source\s).+')
        self.tp_dest = self._get_type(r'(?<=\stranslated-destination\s).+')
        self.service = self._get_type(r'(?<=\sservice\s).+')

    def _get_type(self, pattern):
        match = re.search(pattern, self._policy, flags=re.M)
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
                if 'original' == field:
                    return 'none'
                return field
        return ''
