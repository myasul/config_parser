import regex as re
import csv
import tools.helper as helper
from tools.const import SERVICE_REGEX, SERVICE_FILENAME, FILE_FORMAT


def generate_service_csv(content, csv_dir, file_format):
    services = SERVICE_REGEX.findall(content)
    services_obj = []
    for service in services:
        # Create a list of Address objects
        services_obj.append(Service(service))

    cwd = csv_dir + "/" + SERVICE_FILENAME

    with open(cwd, mode='w+') as parsed_config:
        config_writer = csv.writer(
            parsed_config, delimiter=FILE_FORMAT.get(file_format, ','))
        # Write headers
        config_writer.writerow([
            'service-object', 'protocol', 'destination-port'])

        # Write address entries
        for service in services_obj:
            config_writer.writerow([
                service.get_service_name(),
                service.get_protocol(),
                service.get_destination_port()])


class Service:
    def __init__(self, service):
        self._service = service
        self._service_name = ""
        self._protocol = ""
        self._destination_port = ""
        self.populate_fields()

    # Populate fields by extracting the needed data
    # using regular expressions.
    def populate_fields(self):
        self._service_name = helper.extract_field_name(
            self._service, r'(?<=service-object\s)')
        self._extract_network_details()

    def _extract_network_details(self):
        match = re.search(r'(TCP|UDP)\s*(.+)', self._service)

        # Extract protocol
        if match:
            self._protocol = match.group(1) if match.group else ""

            # Extract and format destination port
            if match.group(2):
                port_match = re.search(
                    r"(?P<port1>\d+)[^\d]+(?P<port2>\d+)", match.group(2))
                if port_match:
                    self._destination_port = "{}-{}".format(
                        port_match['port1'], port_match['port2'])

    def get_service_name(self):
        return self._service_name

    def get_destination_port(self):
        return self._destination_port

    def get_protocol(self):
        return self._protocol
