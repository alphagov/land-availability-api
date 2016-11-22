from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import Point
from api.models import CodePoint
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

                    postcode = row[0].strip().replace(' ', '').upper()

                    try:
                        codepoint = CodePoint.objects.get(postcode=postcode)
                    except CodePoint.DoesNotExist:
                        codepoint = CodePoint()
                        codepoint.postcode = postcode

                    codepoint.quality = row[1]
                    codepoint.point = Point(
                        float(row[2]), float(row[3]), srid=27700)
                    codepoint.country = row[4]
                    codepoint.nhs_region = row[5]
                    codepoint.nhs_health_authority = row[6]
                    codepoint.county = row[7]
                    codepoint.district = row[8]
                    codepoint.ward = row[9]

                    try:
                        codepoint.save()
                    except Exception as e:
                        print('Could not add: {0}'.format(row))
