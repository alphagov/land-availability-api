from django.contrib.gis.geos import Point
from api.models import TrainStop
from .importers import CSVImportCommand


class Command(CSVImportCommand):
    help = 'Import trains stops from a CSV file'

    def __init__(self):
        super().__init__(skip_header=True)

    def process_row(self, row):
        print(row)

        try:
            train_stop = TrainStop.objects.get(atcode_code=row[0])
        except TrainStop.DoesNotExist:
            train_stop = TrainStop()
            train_stop.atcode_code = row[0]

        train_stop.naptan_code = row[1]
        train_stop.point = Point(float(row[2]), float(row[3]), srid=27700)
        train_stop.name = row[4]
        train_stop.main_road = row[5]
        train_stop.side_road = row[6]
        train_stop.type = row[7]
        train_stop.nptg_code = row[8]
        train_stop.local_reference = row[9]

        try:
            train_stop.save()
            train_stop.update_close_locations()
        except Exception as e:
            print('Could not add: {0} because {1}'.format(row, e))
