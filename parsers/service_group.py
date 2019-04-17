import regex as re
import csv

# Import tools
import tools.helper as helper
from tools.logger import get_logger
from tools.const import SERVICE_GRP_FILENAME, SERVICE_GRP_REGEX, FILE_FORMAT


def generate_service_grp_csv(content, csv_dir, file_format):
    logger = get_logger(__name__)
    logger.info("Generating Service Group CSV file.")

    service_grps = SERVICE_GRP_REGEX.findall(content)
    services_grp_obj = []

    parse_count = 0
    for grp in service_grps:
        # Create a list of Service Group objects
        logger.debug("Parsing row {}: {}.".format(parse_count, grp))
        services_grp_obj.append(ServiceGroup(grp, logger))
        logger.debug('Parsing row {} complete.'.format(parse_count))

        parse_count += 1

    cwd = csv_dir + "/" + SERVICE_GRP_FILENAME

    with open(cwd, mode='w+') as parsed_config:
        config_writer = csv.writer(
            parsed_config, delimiter=FILE_FORMAT.get(file_format, ','))
        # Write headers
        config_writer.writerow([
            'name', 'members'])

        # Write address entries
        row_count = 1
        for grp in services_grp_obj:
            grp_content = [
                grp.group_name,
                grp.services]

            logger.debug("Adding row {}. Contains {}.".format(
                row_count, grp_content))

            config_writer.writerow(grp_content)
            row_count += 1

        logger.info("Generating Service Group CSV completed.")


class ServiceGroup:
    def __init__(self, service_group, logger):
        self._service_group = service_group
        self._logger = logger
        self.group_name = ""
        self.services = ""
        self.populate_fields()

    # Populate fields by extracting the needed data
    # using regular expressions.
    def populate_fields(self):
        self.group_name = self._extract_group_name()
        self.services = self._extract_services()

        self._logger.debug("Parsed value: {}".format([
            self.group_name,
            self.services]))

    def _extract_services(self):
        matches = re.findall(r'(?<=\s+service-(?:object|group)).+(?=\n)',
                             self._service_group, re.I | re.M)
        services = []
        for match in matches:
            service = helper.remove_wrapping_quotes(match.strip())
            services.append(service)

        return','.join(services)

    def _extract_group_name(self):
        group_name = helper.extract_field_name(
            self._service_group, r'(?<=^service-group\s)')
        return "{};".format(group_name)
