import regex as re
import csv
import tools.helper as helper
from tools.const import SERVICE_GRP_FILENAME, SERVICE_GRP_REGEX, FILE_FORMAT


def generate_service_grp_csv(content, csv_dir, file_format):
    service_grps = SERVICE_GRP_REGEX.findall(content)
    services_grp_obj = []
    for grp in service_grps:
        # Create a list of Service Group objects
        services_grp_obj.append(ServiceGroup(grp))

    cwd = csv_dir + "/" + SERVICE_GRP_FILENAME

    with open(cwd, mode='w+') as parsed_config:
        config_writer = csv.writer(
            parsed_config, delimiter=FILE_FORMAT.get(file_format, ','))
        # Write headers
        config_writer.writerow([
            'name', 'members'])

        # Write address entries
        for grp in services_grp_obj:
            config_writer.writerow([
                grp.get_group_name(),
                grp.get_services()])


class ServiceGroup:
    def __init__(self, service_group):
        self._service_group = service_group
        self._group_name = ""
        self._services = ""
        self.populate_fields()

    # Populate fields by extracting the needed data
    # using regular expressions.
    def populate_fields(self):
        self._group_name = helper.extract_field_name(
            self._service_group, r'(?<=service-group\s)')
        self._services = self._extract_services()

    def _extract_services(self):
        matches = re.findall(r'(?<=service-object).+(?=\n)',
                             self._service_group, re.I | re.M)
        services = []
        for match in matches:
            service = helper.remove_wrapping_quotes(match.strip())
            services.append(service)

        return','.join(services)

    def get_group_name(self):
        return self._group_name

    def get_services(self):
        return self._services
