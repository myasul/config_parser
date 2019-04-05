import regex as re
import csv

SERVICE_FILENAME = 'services.csv'
SERVICE_REGEX = re.compile(r'^service-object.+$', re.I | re.M)


def generate_service_csv(content, csv_dir):
    services = SERVICE_REGEX.findall(content)
    services_obj = []
    for service in services:
        # Create a list of Address objects
        services_obj.append(Service(service))

    cwd = csv_dir + "/" + SERVICE_FILENAME

    with open(cwd, mode='w+') as parsed_config:
        config_writer = csv.writer(parsed_config, delimiter=',')
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

    def populate_fields(self):
        self._extract_service_name()
        self._extract_network_details()

    def _extract_service_name(self):
        match = re.search(r'(?<=service-object).+(?=TCP|UDP)',
                          self._service, re.I)
        if match:
            # remove wrapping quotes
            service_name = re.sub(r"^['\"]*(.+?)['\"]*$", r"\1",
                          match.group().strip())
            self._service_name = service_name.strip()

    def _extract_network_details(self):
        match = re.search(r'(TCP|UDP)\s*(.+)', self._service)
        
        # Extract protocol
        if match:
            self._protocol = match.group(1) if match.group else ""

            # Extract and format destination port
            if match.group(2):
                port_match = re.search(r"(\d+)[^\d]+(\d+)", match.group(2))
                if port_match:
                    self._destination_port = "{}-{}".format(port_match.group(1)
                    , port_match.group(2))

    def get_service_name(self):
        return self._service_name

    def get_destination_port(self):
        return self._destination_port

    def get_protocol(self):
        return self._protocol
