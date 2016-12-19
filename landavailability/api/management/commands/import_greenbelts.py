from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import MultiPolygon, Point
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.db.models.functions import Centroid
import json
from api.models import Greenbelt


class Command(BaseCommand):
    help = 'Import greenbelt data from a JSON file'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str)

    def handle(self, *args, **options):
        json_file_name = options.get('json_file')

        if json_file_name:
            with open(json_file_name) as jsonfile:
                data = json.load(jsonfile)

            for feature in data['features']:
                self.process_feature(feature)

    def process_feature(self, feature):
        if feature['geometry']['type'] == 'MultiPolygon':
            print('Importing: {0}'.format(feature['id']))

            multi_polygon = GEOSGeometry(
                json.dumps(feature['geometry']), srid=4326)

            try:
                greenbelt = Greenbelt.objects.get(code=feature['id'])
            except Greenbelt.DoesNotExist:
                greenbelt = Greenbelt()
                greenbelt.code = feature['id']

            greenbelt.geom = multi_polygon
            greenbelt.la_name = feature['properties']['LA_Name']
            greenbelt.gb_name = feature['properties']['GB_name']
            greenbelt.ons_code = feature['properties']['ONS_CODE']
            greenbelt.year = feature['properties']['Year']
            greenbelt.area = float(feature['properties']['Area_Ha'])
            greenbelt.perimeter = float(feature['properties']['Perim_Km'])

            try:
                greenbelt.save()
                greenbelt.update_close_locations()
            except Exception as e:
                print('Could not add: {0} because: {1}'.format(
                    greenbelt.code, e))
