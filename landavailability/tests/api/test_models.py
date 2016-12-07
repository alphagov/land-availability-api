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
        self.assertIsNotNone(updated_location.nearest_busstop_distance)

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

    @pytest.mark.django_db
    def test_busstop_pre_delete_signal(self):
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
        location.nearest_busstop = busstop
        location.save()

        self.assertIsNotNone(location.nearest_busstop)

        busstop.delete()

        changed_location = Location.objects.first()
        self.assertIsNone(changed_location.nearest_busstop)
        self.assertEqual(changed_location.nearest_busstop_distance, 0)


class TestLocationModel(TestCase):
    @pytest.mark.django_db
    def test_update_nearest_busstop_on_new_location(self):
        busstop = BusStop()
        busstop.name = 'Test BusStop'
        busstop.point = Point(-2.4153695332751557, 53.585971152959274)
        busstop.save()

        location = Location()
        location.name = 'Test Location'
        geometry = """
            {"coordinates": [
                [
                    [
                        [-2.417243587559938, 53.587307594998805],
                        [-2.4172773190316676, 53.587280070692486],
                        [-2.4173514409852657, 53.58721825948106],
                        [-2.4173514409852657, 53.58721825948106],
                        [-2.417384428573676, 53.58719109717106],
                        [-2.417386408047504, 53.58718974239604],
                        [-2.417388763821763, 53.58718865588064],
                        [-2.417391496782378, 53.58718792747945],
                        [-2.417394356948235, 53.58718746820736],
                        [-2.417397345205334, 53.587187367918965],
                        [-2.417400337006054, 53.587187627048955],
                        [-2.4174030832552806, 53.587188246466916],
                        [-2.4174057076147375, 53.58718913588342],
                        [-2.4174557446310443, 53.587211066209946],
                        [-2.417457873460361, 53.587212226928386],
                        [-2.4174596313048182, 53.587213658515026],
                        [-2.417460892730692, 53.58721527155018],
                        [-2.417461656851856, 53.58721697617914],
                        [-2.417461798234508, 53.58721868298221],
                        [-2.417461442312349, 53.587220481379084],
                        [-2.4174603373317, 53.587222102675575],
                        [-2.4174588578217557, 53.58722363542186],
                        [-2.417425864940114, 53.58725025862445],
                        [-2.417425864940114, 53.58725025862445],
                        [-2.4173494967466667, 53.58731162843292],
                        [-2.4173157608682145, 53.58733870348632],
                        [-2.4173137804994558, 53.58733996840554],
                        [-2.4173114247148657, 53.58734105491944],
                        [-2.4173088162910576, 53.58734178288413],
                        [-2.417305956113853, 53.58734224215419],
                        [-2.4173029678456346, 53.58734234244034],
                        [-2.4173001005826373, 53.58734208287329],
                        [-2.417297355210633, 53.58734155330762],
                        [-2.417294730843975, 53.58734066388879],
                        [-2.417246949791007, 53.58732016334699],
                        [-2.417244820961996, 53.58731900262481],
                        [-2.4172429385723864, 53.58731757146959],
                        [-2.4172416771517287, 53.58731595843215],
                        [-2.417240913037613, 53.587314253801786],
                        [-2.41724077166351, 53.58731254699851],
                        [-2.4172411275957963, 53.587310748602285],
                        [-2.417242107153561, 53.58730903788777],
                        [-2.417243587559938, 53.587307594998805]
                    ]
                ]
            ],
            "type": "MultiPolygon"}
        """

        location.geom = GEOSGeometry(geometry, srid=4326)
        location.point = location.geom.centroid
        location.save()

        saved_location = Location.objects.first()

        self.assertIsNotNone(saved_location.nearest_busstop)
        self.assertTrue(saved_location.nearest_busstop_distance > 0)
