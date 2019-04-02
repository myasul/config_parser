import regex as re
import csv

SERVICE_FILENAME = 'services.csv'
SERVICE_REGEX = re.compile(r'^service-object.+$', re.I | re.M)


def generate_service_csv(content):
    services = SERVICE_REGEX.findall(content)
    services_obj = []
    for service in services:
        # Create a list of Address objects
        services_obj.append(Service(service))

    with open(SERVICE_FILENAME, mode='w+') as parsed_config:
        config_writer = csv.writer(parsed_config, delimiter=',')
        # Write headers
        config_writer.writerow([
            'service name', 'udp', 'tcp'])

        # Write address entries
        for service in services_obj:
            config_writer.writerow([
                service.get_service_name(),
                service.get_tcp(),
                service.get_udp()])


class Service:
    def __init__(self, service):
        self.service = service
        self.service_name = ""
        self.tcp = ""
        self.udp = ""

    def get_service_name(self):
        match = re.search(r'(?<=service-object).+(?=TCP|UDP)',
                          self.service, re.I)
        if match:
            self.service_name = match.group().strip()

        return self.service_name

    def get_tcp(self):
        self.get_service_name()  # Make sure 'service name' variable is set
        match = re.search(r'(?<={}\sTCP).+(?=$)'.format(self.service_name),
                          self.service, re.I)
        if match:
            self.tcp = match.group().strip()

        return self.tcp

    def get_udp(self):
        self.get_service_name()  # Make sure 'service name' variable is set
        match = re.search(r'(?<={}\sUDP).+(?=$)'.format(self.service_name),
                          self.service, re.I)
        if match:
            self.udp = match.group().strip()

        return self.udp
