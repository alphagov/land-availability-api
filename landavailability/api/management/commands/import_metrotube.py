from django.contrib.gis.geos import Point
from api.models import MetroTube
from .importers import CSVImportCommand


class Command(CSVImportCommand):
    help = 'Import Metro and Tube from a CSV file'

    def __init__(self):
        super().__init__(skip_header=True, encoding='ISO-8859-1')

    def process_row(self, row):
        print('{0} - {1}'.format(row[0], row[4]))

        # Only import Metro and Tube
        if row[31] == 'TMU':
            try:
                metrotube = MetroTube.objects.get(atco_code=row[0])
            except MetroTube.DoesNotExist:
                metrotube = MetroTube()
                metrotube.atco_code = row[0]

            metrotube.naptan_code = row[2]
            metrotube.name = row[4]
            metrotube.locality = row[18]
            metrotube.point = Point(float(row[29]), float(row[30]), srid=4326)

            try:
                metrotube.save()
                # metrotube.update_close_locations()
            except Exception as e:
                print('Could not add: {0} because {1}'.format(row, e))
