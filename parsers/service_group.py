import regex as re
import csv

SERVICE_GRP_FILENAME = 'service-group.csv'
SERVICE_GRP_REGEX = re.compile(r'^service-group.+?exit$', re.I | re.M | re.S)


def generate_service_grp_csv(content, csv_dir):
    service_grps = SERVICE_GRP_REGEX.findall(content)
    services_grp_obj = []
    for grp in service_grps:
        # Create a list of Service Group objects
        services_grp_obj.append(ServiceGroup(grp))

    cwd = csv_dir + "/" + SERVICE_GRP_FILENAME

    with open(cwd, mode='w+') as parsed_config:
        config_writer = csv.writer(parsed_config, delimiter=',')
        # Write headers
        config_writer.writerow([
            'service group name', 'service'])

        # Write address entries
        for grp in services_grp_obj:
            if len(grp.get_services()) > 0:
                for service in grp.get_services():
                    config_writer.writerow([
                        grp.get_group_name(),
                        service])
            else:
                config_writer.writerow([
                    grp.get_group_name(),
                    ""
                ])


class ServiceGroup:
    def __init__(self, service_group):
        self.service_group = service_group
        self.group_name = ""
        self.services = []

    def get_group_name(self):
        match = re.search(r'(?<=service-group).+(?=\n)',
                          self.service_group, re.I)
        if match:
            self.service_name = match.group().strip()

        return self.service_name

    def get_services(self):
        self.services = []
        matches = re.findall(r'(?<=service-object).+(?=\n)',
                             self.service_group, re.I | re.M)
        for match in matches:
            self.services.append(match.strip())

        return self.services
