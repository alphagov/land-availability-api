from django.core.management.base import BaseCommand, CommandError
import csv


class CSVImportCommand(BaseCommand):
    help = 'Import data from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def process_row(self, row):
        pass

    def handle(self, *args, **options):
        csv_file_name = options.get('csv_file')

        if csv_file_name:
            with open(csv_file_name, newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=',', quotechar='"')

                for row in reader:
                    self.process_row(row)
