from django.contrib.gis.geos import GEOSGeometry
from api.models import Substation
from .importers import ShapefileImportCommand
import json


class Command(ShapefileImportCommand):
    help = 'Import Substations from a *.shp file'

    def process_record(self, record):
        if record.shape.__geo_interface__['type'] == 'Polygon':
            print(record.record)

            try:
                substation = Substation.objects.get(name=record.record[0])
            except Substation.DoesNotExist:
                substation = Substation()
                substation.name = record.record[0]

            substation.operating = record.record[1]
            substation.action_dtt = record.record[2]
            substation.status = record.record[3]
            substation.description = record.record[4]
            substation.owner_flag = record.record[5]
            substation.gdo_gid = record.record[6]

            substation.geom = GEOSGeometry(
                    json.dumps(record.shape.__geo_interface__), srid=27700)

            try:
                substation.save()
                substation.update_close_locations()
            except Exception as e:
                print('Could not add: {0}'.format(record.record))
