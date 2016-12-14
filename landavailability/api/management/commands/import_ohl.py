from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos import MultiLineString, LineString
from .importers import ShapefileImportCommand
from api.models import OverheadLine
import json


class Command(ShapefileImportCommand):
    help = 'Import Overhead Lines from a *.shp file'

    def process_record(self, record):
        print(record.record)

        try:
            ohl = OverheadLine.objects.get(gdo_gid=record.record[0])
        except OverheadLine.DoesNotExist:
            ohl = OverheadLine()
            ohl.gdo_gid = record.record[0]

        ohl.route_asset = record.record[1]
        ohl.towers = record.record[2]
        ohl.action_dtt = record.record[3]
        ohl.status = record.record[4]
        ohl.operating = record.record[5]
        ohl.circuit_1 = record.record[6]
        ohl.circuit_2 = record.record[7]
        ohl.geom = GEOSGeometry(
                json.dumps(record.shape.__geo_interface__), srid=27700)

        try:
            ohl.save()
            ohl.update_close_locations()
        except Exception as e:
            print('Could not add: {0}'.format(record.record))
