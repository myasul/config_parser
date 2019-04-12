import regex as re
import csv

# Import tools
import tools.helper as helper
from tools.logger import get_logger
from tools.const import SERVICE_REGEX, SERVICE_FILENAME, FILE_FORMAT


def generate_service_csv(content, csv_dir, file_format):
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
                service.get_service_name(),
                service.get_protocol(),
                service.get_destination_port()]

            logger.debug("Adding row {}. Contains {}".format(
                row_count, service_content))

            config_writer.writerow(service_content)


class Service:
    def __init__(self, service, logger):
        self._service = service
        self._service_name = ""
        self._protocol = ""
        self._destination_port = ""
        self._logger = logger
        self.populate_fields()

    # Populate fields by extracting the needed data
    # using regular expressions.
    def populate_fields(self):
        self._service_name = helper.extract_field_name(
            self._service, r'(?<=service-object\s)')
        self._extract_network_details()

        self._logger.debug("Parsed value: {}".format([
            self.get_service_name(),
            self.get_protocol(),
            self.get_destination_port()
        ]))

    def _extract_network_details(self):
        match = re.search(
            r'\s+(?P<protocol>TCP|UDP|ICMPV6|ICMP)\s+(?P<ports>.+)',
            self._service)

        # If the protocol is not included in the list of protocol in the
        # previous regex, try to extract the protocol and ports using
        # the regex below
        if not match:
            match = re.search(r'(service-object\s((""[^"]+"")|[^\s]+)\s)' +
                              r'(?P<protocol>[^\s]+)\s+(?P<ports>.+)',
                              self._service)

        # Validate if all network columns have been extracted
        if match:
            network_details = match.groupdict()
            # Extract protocol
            self._protocol = helper.remove_wrapping_quotes(
                network_details.get('protocol'))

            # Extract and format destination port
            if network_details.get('ports'):
                port_match = re.search(
                    r"^(?P<port1>\d+)[^\d]+(?P<port2>\d+)",
                    network_details.get('ports').strip())
                if port_match:
                    destination_port = "{}-{}".format(
                        port_match['port1'], port_match['port2'])
                    self._destination_port = helper.remove_wrapping_quotes(
                        destination_port)

    def get_service_name(self):
        return self._service_name

    def get_destination_port(self):
        return self._destination_port

    def get_protocol(self):
        return self._protocol
