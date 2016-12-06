from django.contrib.gis.geos import Point
from api.models import BusStop
from .importers import CSVImportCommand


class Command(CSVImportCommand):
    help = 'Import bus stops from a CSV file'

    def process_row(self, row):
        print(row)

        try:
            bus_stop = BusStop.objects.get(amic_code=row[0])
        except BusStop.DoesNotExist:
            bus_stop = BusStop()
            bus_stop.amic_code = row[0]

        bus_stop.point = Point(float(row[2]), float(row[3]), srid=27700)
        bus_stop.name = row[4]
        bus_stop.direction = row[5]
        bus_stop.area = row[6]
        bus_stop.road = row[7]
        bus_stop.nptg_code = row[9]

        try:
            bus_stop.save()
            bus_stop.update_close_locations()
        except Exception as e:
            print('Could not add: {0}'.format(row))
