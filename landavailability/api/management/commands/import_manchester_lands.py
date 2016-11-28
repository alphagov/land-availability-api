from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import MultiPolygon, Point
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.db.models.functions import Centroid
import json
from api.models import Location


class Command(BaseCommand):
    help = 'Import land data for Manchester from a JSON file'

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
            multi_polygon = GEOSGeometry(
                json.dumps(feature['geometry']), srid=3857)

            try:
                location = Location.objects.get(
                    name=feature['properties']['address'],
                    geom=multi_polygon)
            except Location.DoesNotExist:
                location = Location()
                location.name = feature['properties']['address']
                location.geom = multi_polygon

            location.point = location.geom.centroid
            location.authority = feature['properties']['la']
            location.owner = feature['properties']['la']

            try:
                location.save()
            except Exception as e:
                print('Could not add: {0} because: {1}'.format(
                    location.name, e))
