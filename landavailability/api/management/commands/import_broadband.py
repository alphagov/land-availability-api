from django.contrib.gis.geos import Point
from api.models import CodePoint, Broadband
from .importers import CSVImportCommand
from .utils import get_codepoint_from_postcode


class Command(CSVImportCommand):
    help = 'Import broadband information from a CSV file'

    def __init__(self):
        super().__init__(skip_header=True)

    def clean_column(self, column):
        clean = column.replace('<', '').replace('N/A', '')

        if clean == '':
            return '0'
        else:
            return clean

    def process_row(self, row):
        print(row)

        codepoint = get_codepoint_from_postcode(row[0])

        if codepoint:
            try:
                broadband = Broadband.objects.get(postcode=row[0])
            except Broadband.DoesNotExist:
                broadband = Broadband()
                broadband.postcode = row[0]

            broadband.point = codepoint.point
            broadband.speed_30_mb_percentage = float(row[2])
            broadband.avg_download_speed = float(self.clean_column(row[7]))
            broadband.min_download_speed = float(self.clean_column(row[9]))
            broadband.max_download_speed = float(self.clean_column(row[10]))
            broadband.avg_upload_speed = float(self.clean_column(row[15]))
            broadband.min_upload_speed = float(self.clean_column(row[17]))
            broadband.max_upload_speed = float(self.clean_column(row[18]))

            try:
                broadband.save()
                broadband.update_close_locations()
            except Exception as e:
                print('Could not add: {0}'.format(row))
        else:
            print(
                'Could not add: {0} because codepoint information'
                ' is missing'.format(row))
