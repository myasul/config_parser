import regex as re
import csv

# Import tools
import tools.helper as helper
from tools.logger import get_logger
from tools.const import ZONE_REGEX, ZONE_FILENAME, FILE_FORMAT


def generate_zone_csv(content, csv_dir, file_format):
    logger = get_logger(__name__)
    logger.info("Generating Zone CSV file.")

    zones = ZONE_REGEX.findall(content)
    zones_obj = []

    parse_count = 0
    for zone in zones:
        # Create a list of Address objects
        logger.debug("Parsing row {}: {}.".format(parse_count, zone))
        zones_obj.append(Zone(zone, logger))
        logger.debug("Parsing row {} complete.".format(parse_count))

    cwd = csv_dir + "/" + ZONE_FILENAME

    with open(cwd, mode='w+') as parsed_config:
        config_writer = csv.writer(
            parsed_config, delimiter=FILE_FORMAT.get(file_format, ','))
        # Write headers
        config_writer.writerow([
            'zone', 'name'])

        # Write address entries
        row_count = 1
        for zone in zones_obj:
            zone_content = [
                zone.zone,
                zone.name, ]

            logger.debug("Adding row {}. Contains {}".format(
                row_count, zone_content))

            config_writer.writerow(zone_content)


class Zone:
    def __init__(self, zone_config, logger):
        self._zone_config = zone_config
        self._logger = logger
        self.zone = "zone"
        self.name = ""
        self.populate_fields()

    # Populate fields by extracting the needed data
    # using regular expressions.
    def populate_fields(self):
        self.name = helper.extract_field_name(
            self._zone_config, r'(?<=zone\s)')

        self._logger.debug("Parsed value: {}".format([
            self.zone,
            self.name,
        ]))
