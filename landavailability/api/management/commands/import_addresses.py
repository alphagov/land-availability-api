from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import Point
from api.models import Address
import csv


class Command(BaseCommand):
    help = 'Import addresses from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **options):
        csv_file_name = options.get('csv_file')

        if csv_file_name:
            with open(csv_file_name, newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=',', quotechar='"')

                for row in reader:
                    print(row)

                    try:
                        address = Address.objects.get(uprn=row[0])
                    except Address.DoesNotExist:
                        address = Address()
                        address.uprn = row[0]

                    address.address_line_1 = row[2]
                    address.address_line_2 = row[3]
                    address.address_line_3 = row[4]
                    address.city = row[5]
                    address.county = row[6]
                    address.postcode = row[7]
                    address.country_code = row[8]
                    address.point = Point(float(row[10]), float(row[9]))

                    try:
                        address.save()
                    except Exception as e:
                        print('Could not add: {0}'.format(row))
