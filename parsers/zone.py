import regex as re
import csv

# Import tools
import tools.helper as helper
from tools.logger import get_logger
from tools.const import ZONE_REGEX, ZONE_FILENAME, FILE_FORMAT


def generate_zone_csv(content, csv_dir, file_format):
    """Process the configuration file and create the zone.csv file.

    The method would extract all the zone lines in the provided config
    file. Every zone line would be save as Zone object for further
    extraction. After further extraction every Zone object would be saved
    in the zone.csv.

    Args:
        content: Data as string coming from the configuration file.
        csv_dir: Directory where the zone.csv would be saved.
        file_format: zone file can be saved as .csv or .ssv.

    Returns:
        None

    """
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
    """Extracted zone line would be further processed in this class.

    Columns that should be displayed in the zone.csv would be extracted
    using regular expressions and would be saved in the class attributes.

    Attributes:
        zone_config: The zone line to be processed.
        logger: use for logging purposes
        zone: e.g. zone
        name: e.g. MULTICAST

    """

    def __init__(self, zone_config, logger):
        """Initialize columns."""
        self._zone_config = zone_config
        self._logger = logger
        self.zone = "zone"
        self.name = ""
        self.populate_fields()

    def populate_fields(self):
        """Populate fields by extracting the needed data using regex."""
        self.name = helper.extract_field_name(
            self._zone_config, r'(?<=zone\s)')

        self._logger.debug("Parsed value: {}".format([
            self.zone,
            self.name,
        ]))
