from django.contrib.gis.geos import Point
from api.models import Address
from .importers import CSVImportCommand


class Command(CSVImportCommand):
    help = 'Import addresses from a CSV file'

    def process_row(self, row):
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
        address.postcode = row[7].strip().replace(' ', '').upper()
        address.country_code = row[8]
        address.point = Point(float(row[10]), float(row[9]))

        try:
            address.save()
        except Exception as e:
            print('Could not add: {0}'.format(row))
