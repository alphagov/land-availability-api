from unittest import TestCase
import pytest
import json
from django.contrib.gis.geos import Point
from django.contrib.gis.geos import GEOSGeometry
from api.models import BusStop, Location


class TestBusStopModel(TestCase):
    @pytest.mark.django_db
    def test_update_location_no_busstop(self):
        busstop = BusStop()
        busstop.name = 'Test BusStop'
        busstop.point = Point(-2.347743000012108, 53.38737090322739)
        busstop.save()

        location = Location()
        location.name = 'Test Location'
        geometry = """
            {"coordinates": [
                [
                    [
                        [-2.373605477415186, 53.40969504659278],
                        [-2.3737618172100063, 53.409339507361864],
                        [-2.3736420825281206, 53.409349059663356],
                        [-2.3736136182503316, 53.40925098435937],
                        [-2.372348437061216, 53.40941673318565],
                        [-2.3723238976272407, 53.409362878222495],
                        [-2.371773640845859, 53.40943257437743],
                        [-2.3718032009919567, 53.40951191448939],
                        [-2.3718245008682466, 53.40956909854221],
                        [-2.3718353336832725, 53.4095981768949],
                        [-2.372388619083221, 53.40952876960275],
                        [-2.372366986029961, 53.40974214341905],
                        [-2.37244330450709, 53.40977355411032],
                        [-2.3724480893933726, 53.40980293194619],
                        [-2.3730546640198655, 53.40984058711081],
                        [-2.3730816588728425, 53.409842195613976],
                        [-2.373519931021509, 53.40988946797718],
                        [-2.3736042816221192, 53.409901787986364],
                        [-2.3736898279409133, 53.40970736641803],
                        [-2.373605477415186, 53.40969504659278]
                    ]
                ]
            ],
            "type": "MultiPolygon"}
        """
        location.geom = GEOSGeometry(geometry, srid=4326)
        location.point = location.geom.centroid
        location.save()

        busstop.update_close_locations(distance=3000)

        updated_location = Location.objects.first()
        self.assertEqual(
            updated_location.nearest_busstop.name,
            'Test BusStop')

    @pytest.mark.django_db
    def test_update_location_busstop_distance(self):
        busstop = BusStop()
        busstop.name = 'Test BusStop'
        busstop.point = Point(-2.347743000012108, 53.38737090322739)
        busstop.save()

        location = Location()
        location.name = 'Test Location'
        geometry = """
            {"coordinates": [
                [
                    [
                        [-2.373605477415186, 53.40969504659278],
                        [-2.3737618172100063, 53.409339507361864],
                        [-2.3736420825281206, 53.409349059663356],
                        [-2.3736136182503316, 53.40925098435937],
                        [-2.372348437061216, 53.40941673318565],
                        [-2.3723238976272407, 53.409362878222495],
                        [-2.371773640845859, 53.40943257437743],
                        [-2.3718032009919567, 53.40951191448939],
                        [-2.3718245008682466, 53.40956909854221],
                        [-2.3718353336832725, 53.4095981768949],
                        [-2.372388619083221, 53.40952876960275],
                        [-2.372366986029961, 53.40974214341905],
                        [-2.37244330450709, 53.40977355411032],
                        [-2.3724480893933726, 53.40980293194619],
                        [-2.3730546640198655, 53.40984058711081],
                        [-2.3730816588728425, 53.409842195613976],
                        [-2.373519931021509, 53.40988946797718],
                        [-2.3736042816221192, 53.409901787986364],
                        [-2.3736898279409133, 53.40970736641803],
                        [-2.373605477415186, 53.40969504659278]
                    ]
                ]
            ],
            "type": "MultiPolygon"}
        """
        location.geom = GEOSGeometry(geometry, srid=4326)
        location.point = location.geom.centroid
        location.save()

        busstop.update_close_locations(distance=3000)

        updated_location = Location.objects.first()
        updated_location.refresh_busstop_distance()

        self.assertIsNotNone(updated_location.nearest_busstop_distance)
