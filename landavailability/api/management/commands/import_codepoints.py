from django.contrib.gis.geos import Point
from api.models import CodePoint
from .importers import CSVImportCommand


class Command(CSVImportCommand):
    help = 'Import codepoints from a CSV file'

    def process_row(self, row):
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
