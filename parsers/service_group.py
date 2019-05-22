import regex as re
import csv

# Import tools
import tools.helper as helper
from tools.logger import get_logger
from tools.const import SERVICE_GRP_FILENAME, SERVICE_GRP_REGEX, FILE_FORMAT


def generate_service_grp_csv(content, csv_dir, file_format):
    """Process the configuration file and create the service_group.csv file.

    The method would extract all the service_group lines in the provided config
    file. Every service_group line would be save as ServiceGroup object for
    further extraction. After further extraction every ServiceGroup object
    would be saved in the service_group.csv.

    Args:
        content: Data as string coming from the configuration file.
        csv_dir: Directory where the service_group.csv would be saved.
        file_format: service_group file can be saved as .csv or .ssv.

    Returns:
        None

    """
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
    """Extracted service_group line would be further processed in this class.

    Columns that should be displayed in the service_group.csv would be
    extracted using regular expressions and would be saved in the class
    attributes.

    Attributes:
        service_group: The service_group line to be processed.
        logger: use for logging purposes
        group_name: e.g. AD Directory Services
        services: list of services that are comma separated.
            e.g. Terminal Services TCP,Terminal Services UDP

    """

    def __init__(self, service_group, logger):
        """Initialize columns."""
        self._service_group = service_group
        self._logger = logger
        self.group_name = ""
        self.services = ""
        self.populate_fields()

    def populate_fields(self):
        """Populate fields by extracting the needed data using regex."""
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
