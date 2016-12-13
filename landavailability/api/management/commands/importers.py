from django.core.management.base import BaseCommand, CommandError
import csv
import shapefile


class CSVImportCommand(BaseCommand):
    help = 'Import data from a CSV file'

    def __init__(self, skip_header=False):
        self.skip_header = skip_header

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def process_row(self, row):
        pass

    def handle(self, *args, **options):
        csv_file_name = options.get('csv_file')

        if csv_file_name:
            with open(csv_file_name, newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=',', quotechar='"')

                if self.skip_header:
                    next(reader)

                for row in reader:
                    self.process_row(row)


class ShapefileImportCommand(BaseCommand):
    help = 'Import data from a *.shp file'

    def add_arguments(self, parser):
        parser.add_argument('shp_file', type=str)

    def process_record(self, record):
        pass

    def handle(self, *args, **options):
        shp_file_name = options.get('shp_file')

        if shp_file_name:
            reader = shapefile.Reader(shp_file_name)
            for record in reader.shapeRecords():
                if record.shape.shapeType == shapefile.NULL:
                    continue
                self.process_record(record)
