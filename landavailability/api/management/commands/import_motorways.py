from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos import MultiLineString, LineString
from .importers import ShapefileImportCommand
from api.models import Motorway
import json


class Command(ShapefileImportCommand):
    help = 'Import Motorways from a *.shp file'

    def process_record(self, record):
        print(record.record)

        try:
            mw = Motorway.objects.get(identifier=record.record[0])
        except Motorway.DoesNotExist:
            mw = Motorway()
            mw.identifier = record.record[0]

        mw.number = record.record[1]
        mw.point = GEOSGeometry(
                json.dumps(record.shape.__geo_interface__), srid=27700)

        try:
            mw.save()
            mw.update_close_locations()
        except Exception as e:
            print('Could not add: {0}'.format(record.record))
