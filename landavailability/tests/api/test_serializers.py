from unittest import TestCase
import pytest
import json
from django.contrib.gis.geos import Point
from api.models import (
    BusStop, TrainStop, Address, CodePoint, Broadband, MetroTube, Greenbelt)
from api.serializers import (
    BusStopSerializer, TrainStopSerializer, AddressSerializer,
    CodePointSerializer, BroadbandSerializer, MetroTubeSerializer,
    GreenbeltSerializer)


class TestBusStopSerializer(TestCase):
    @pytest.mark.django_db
    def test_busstop_serializer_create_object(self):
        json_payload = """
            {
                "amic_code": "1800AMIC001",
                "point": {
                    "type": "Point",
                    "coordinates": [-2.347743000012108,53.38737090322739]
                },
                "name": "Altrincham Interchange",
                "direction": "Nr Train Station",
                "area": "NA",
                "road": "STAMFORD NEW RD",
                "nptg_code": "E0028261",
                "srid": 4326
            }
        """

        data = json.loads(json_payload)
        serializer = BusStopSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        serializer.save()
        self.assertEqual(BusStop.objects.count(), 1)


class TestTrainStopSerializer(TestCase):
    @pytest.mark.django_db
    def test_trainstop_serializer_create_object(self):
        json_payload = """
            {
                "atcode_code": "9100ALTRNHM",
                "naptan_code": "",
                "point": {
                    "type": "Point",
                    "coordinates": [377008, 387924]
                },
                "name": "DATALAND INTERCHANGE",
                "main_road": "DATALAND NEW RD",
                "side_road": "DATA LANE",
                "type": "R",
                "nptg_code": "E0028261",
                "local_reference": "AA123ZZ",
                "srid": 27700
            }
        """

        data = json.loads(json_payload)
        serializer = TrainStopSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        serializer.save()
        self.assertEqual(TrainStop.objects.count(), 1)


class TestAddressSerializer(TestCase):
    @pytest.mark.django_db
    def test_address_serializer_create_object(self):
        json_payload = """
            {
                "uprn": "12345678",
                "address_line_1": "Dataland",
                "address_line_2": "Dataland Village Main Street",
                "city": "Dataland City",
                "county": "Cucumberland",
                "postcode": "AA11 1ZZ",
                "country_code": "GB",
                "point": {
                    "type": "Point",
                    "coordinates": [55.4168769443259, -1.83356713993623]
                },
                "srid": 4326
            }
        """

        data = json.loads(json_payload)
        serializer = AddressSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        serializer.save()
        self.assertEqual(Address.objects.count(), 1)


class TestCodePointSerializer(TestCase):
    @pytest.mark.django_db
    def test_codepoint_serializer_create_object(self):
        json_payload = """
            {
                "postcode": "BL0 0AA",
                "quality": "10",
                "country": "E92000001",
                "nhs_region": "E19000001",
                "nhs_health_authority": "E18000002",
                "county": "",
                "district": "E08000002",
                "ward": "E05000681",
                "point": {
                    "type": "Point",
                    "coordinates": [379448, 416851]
                },
                "srid": 27700
            }
        """

        data = json.loads(json_payload)
        serializer = CodePointSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        serializer.save()
        self.assertEqual(CodePoint.objects.count(), 1)


class TestBroadbandSerializer(TestCase):
    @pytest.mark.django_db
    def test_broadband_serializer_create_object(self):
        # Prepare a CodePoint
        codepoint = CodePoint()
        codepoint.postcode = 'ME58TL'
        codepoint.point = Point(
            float("-1.83356713993623"), float("55.4168769443259"))
        codepoint.quality = 10
        codepoint.save()

        json_payload = """
            {
                "postcode": "ME5 8TL",
                "speed_30_mb_percentage": 50,
                "avg_download_speed": 10.5,
                "min_download_speed": 2.8,
                "max_download_speed": 12.3,
                "avg_upload_speed": 0.5,
                "min_upload_speed": 0.3,
                "max_upload_speed": 1.1
            }
        """

        data = json.loads(json_payload)
        serializer = BroadbandSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        serializer.save()
        self.assertEqual(Broadband.objects.count(), 1)

    @pytest.mark.django_db
    def test_broadband_invalid_serializer_no_codepoint(self):
        json_payload = """
            {
                "postcode": "ME5 8TL",
                "speed_30_mb_percentage": 50,
                "avg_download_speed": 10.5,
                "min_download_speed": 2.8,
                "max_download_speed": 12.3,
                "avg_upload_speed": 0.5,
                "min_upload_speed": 0.3,
                "max_upload_speed": 1.1
            }
        """

        data = json.loads(json_payload)
        serializer = BroadbandSerializer(data=data)
        self.assertFalse(serializer.is_valid())


class TestMetroTubeSerializer(TestCase):
    @pytest.mark.django_db
    def test_metrotube_serializer_create_object(self):
        json_payload = """
            {
                "atco_code": "1800AMIC001",
                "name": "Altrincham Interchange",
                "naptan_code": "bsstnxl",
                "locality": "",
                "point": {
                    "type": "Point",
                    "coordinates": [-2.347743000012108,53.38737090322739]
                },
                "srid": 4326
            }
        """

        data = json.loads(json_payload)
        serializer = MetroTubeSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        serializer.save()
        self.assertEqual(MetroTube.objects.count(), 1)


class TestGreenbeltSerializer(TestCase):
    @pytest.mark.django_db
    def test_greenbelt_serializer_create_object(self):
        json_payload = """
            {
                "code": "Local_Authority_green_belt_boundaries_2014-15.25",
                "la_name": "City of Stoke-on-Trent (B)",
                "gb_name": "Stoke Greenbelt",
                "ons_code": "E06000021",
                "year": "2014/15",
                "area": 50.1,
                "perimeter": 120.23,
                "geom": {
                    "type": "MultiPolygon",
                    "coordinates": [
                    [
                        [
                        [
                            -2.1614837256814963,
                            53.07183331520438,
                            0
                        ],
                        [
                            -2.161440204004493,
                            53.07167876512527,
                            0
                        ],
                        [
                            -2.161426422046515,
                            53.07158231050548,
                            0
                        ],
                        [
                            -2.161412261861244,
                            53.07128283205548,
                            0
                        ],
                        [
                            -2.161373377871479,
                            53.071211109880664,
                            0
                        ],
                        [
                            -2.161369504865456,
                            53.07118401041043,
                            0
                        ],
                        [
                            -2.1617677327485008,
                            53.07111245525075,
                            0
                        ],
                        [
                            -2.1617682739467705,
                            53.071109120469266,
                            0
                        ],
                        [
                            -2.1620568237599738,
                            53.07147709017702,
                            0
                        ],
                        [
                            -2.162246918923053,
                            53.07170561414385,
                            0
                        ],
                        [
                            -2.162193868651531,
                            53.07171503969784,
                            0
                        ],
                        [
                            -2.162142294698858,
                            53.07172373689699,
                            0
                        ],
                        [
                            -2.1621361236605248,
                            53.07171871503741,
                            0
                        ],
                        [
                            -2.1614837256814963,
                            53.07183331520438,
                            0
                        ]
                        ]
                    ]
                    ]
                },
                "srid": 4326
            }
        """

        data = json.loads(json_payload)
        serializer = GreenbeltSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        serializer.save()
        self.assertEqual(Greenbelt.objects.count(), 1)
