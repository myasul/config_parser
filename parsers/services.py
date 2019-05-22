import regex as re
import csv

# Import tools
import tools.helper as helper
from tools.logger import get_logger
from tools.const import SERVICE_REGEX, SERVICE_FILENAME, FILE_FORMAT


def generate_service_csv(content, csv_dir, file_format):
    """Process the configuration file and create the services.csv file.

    The method would extract all the services lines in the provided config
    file. Every services line would be save as Services object for further
    extraction. After further extraction every Services object would be saved
    in the services.csv.

    Args:
        content: Data as string coming from the configuration file.
        csv_dir: Directory where the services.csv would be saved.
        file_format: services file can be saved as .csv or .ssv.

    Returns:
        None

    """
    logger = get_logger(__name__)
    logger.info("Generating Service CSV file.")

    services = SERVICE_REGEX.findall(content)
    services_obj = []

    parse_count = 0
    for service in services:
        # Create a list of Address objects
        logger.debug("Parsing row {}: {}.".format(parse_count, service))
        services_obj.append(Service(service, logger))
        logger.debug("Parsing row {} complete.".format(parse_count))

    cwd = csv_dir + "/" + SERVICE_FILENAME

    with open(cwd, mode='w+') as parsed_config:
        config_writer = csv.writer(
            parsed_config, delimiter=FILE_FORMAT.get(file_format, ','))
        # Write headers
        config_writer.writerow([
            'service-object', 'protocol', 'destination-port'])

        # Write address entries
        row_count = 1
        for service in services_obj:
            service_content = [
                service.service_name,
                service.protocol,
                service.destination_port]

            logger.debug("Adding row {}. Contains {}".format(
                row_count, service_content))

            config_writer.writerow(service_content)


class Service:
    """Extracted services line would be further processed in this class.

    Columns that should be displayed in the services.csv would be extracted
    using regular expressions and would be saved in the class attributes.

    Attributes:
        services: The services line to be processed.
        logger: use for logging purposes
        service_name: e.g. IMAP3
        protocol: e.g. tcp
        destination_port: e.g. 3389-3389

    """

    def __init__(self, service, logger):
        """Initialize columns."""
        self._service = service
        self._logger = logger
        self.service_name = ""
        self.protocol = ""
        self.destination_port = ""
        self.populate_fields()

    def populate_fields(self):
        """Populate fields by extracting the needed data using regex."""
        self.service_name = helper.extract_field_name(
            self._service, r'(?<=service-object\s)')
        self._extract_network_details()

        self._logger.debug("Parsed value: {}".format([
            self.service_name,
            self.protocol,
            self.destination_port
        ]))

    def _extract_network_details(self):
        """Extract and format both protocol and ports."""
        match = re.search(
            r'\s+(?P<protocol>TCP|UDP|ICMPV6|ICMP)\s+(?P<ports>.+)',
            self._service)

        # If the protocol is not included in the list of protocol in the
        # previous regex, try to extract the protocol and ports using
        # the regex below
        if not match:
            match = re.search(r'(service-object\s((""?[^"]+""?)|[^\s]+)\s)' +
                              r'(?P<protocol>[^\s]+)\s*(?P<ports>.+)?',
                              self._service)

        # Validate if all network columns have been extracted
        if match:
            network_details = match.groupdict()
            # Extract protocol
            protocol = helper.remove_wrapping_quotes(
                network_details.get('protocol'))
            self.protocol = protocol.lower()

            # Extract and format destination port
            if network_details.get('ports'):
                port_match = re.search(
                    r"^(?P<port1>\d+)[^\d]+(?P<port2>\d+)",
                    network_details.get('ports').strip())
                if port_match:
                    destination_port = "{}-{}".format(
                        port_match['port1'], port_match['port2'])
                    self.destination_port = helper.remove_wrapping_quotes(
                        destination_port)
