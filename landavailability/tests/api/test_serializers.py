from unittest import TestCase
import pytest
import json
from django.contrib.gis.geos import Point
from api.models import (
    BusStop, TrainStop, Address, CodePoint, Broadband, MetroTube, Greenbelt,
    Motorway, Substation, OverheadLine, School)
from api.serializers import (
    BusStopSerializer, TrainStopSerializer, AddressSerializer,
    CodePointSerializer, BroadbandSerializer, MetroTubeSerializer,
    GreenbeltSerializer, MotorwaySerializer, SubstationSerializer,
    OverheadLineSerializer, SchoolSerializer)


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

    @pytest.mark.django_db
    def test_metrotube_serializer_create_object_no_naptan(self):
        json_payload = """
            {
                "atco_code": "1800AMIC001",
                "name": "Altrincham Interchange",
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


class TestMotorwaySerializer(TestCase):
    @pytest.mark.django_db
    def test_motorway_serializer_create_object(self):
        json_payload = """
            {
                "identifier": "1800AMIC001",
                "number": "M58",
                "point": {
                    "type": "Point",
                    "coordinates": [-2.347743000012108, 53.38737090322739]
                },
                "srid": 4326
            }
        """

        data = json.loads(json_payload)
        serializer = MotorwaySerializer(data=data)
        self.assertTrue(serializer.is_valid())

        serializer.save()
        self.assertEqual(Motorway.objects.count(), 1)


class TestSubstationSerializer(TestCase):
    @pytest.mark.django_db
    def test_substation_serializer_create_object(self):
        json_payload = """
            {
                "name": "BICF4",
                "operating": "400kV",
                "action_dtt": "20130514",
                "status": "C",
                "description": "BICKER FEN 400KV SUBSTATION",
                "owner_flag": "Y",
                "gdo_gid": "259039",
                "geom": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [-0.22341515058230163, 52.93036769987315],
                            [-0.22039561538021543, 52.93215130879717],
                            [-0.21891135174799967, 52.93122765287705],
                            [-0.22193998154995934, 52.92945074233686],
                            [-0.22341515058230163, 52.93036769987315]
                        ]
                    ]
                },
                "srid": 4326
            }
        """

        data = json.loads(json_payload)
        serializer = SubstationSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        serializer.save()
        self.assertEqual(Substation.objects.count(), 1)


class TestOverheadLineSerializer(TestCase):
    @pytest.mark.django_db
    def test_overheadline_serializer_create_object(self):
        json_payload = """
            {
                "gdo_gid": "43166",
                "route_asset": "YYE",
                "towers": "YYE ROUTE TWR (001 - 023 - ZF134B)",
                "action_dtt": "20140714",
                "status": "C",
                "operating": "275",
                "circuit_1": "BERKSWELL - FECKENHAM",
                "circuit_2": "BERKSWELL - OCKER HILL",
                "geom": {
                    "coordinates":
                        [
                            [-1.7162378414130184, 52.39509813723668],
                            [-1.7118087047460224, 52.39445334104352],
                            [-1.7069444136941159, 52.39381157847583],
                            [-1.7012910833623787, 52.39304704079583],
                            [-1.6974465258080322, 52.39163987225863],
                            [-1.6927458315081603, 52.389897117451085],
                            [-1.6880263699584392, 52.38818563270853],
                            [-1.6837766072452327, 52.386592086779146],
                            [-1.6794755043949512, 52.38495278375084],
                            [-1.6750111100750937, 52.3837364391955],
                            [-1.6689556202008984, 52.38208344308663],
                            [-1.6642786485153964, 52.38081164222021],
                            [-1.6592208948258016, 52.379421687420404],
                            [-1.6539729824641247, 52.377968028322485],
                            [-1.6496342378207944, 52.37675956612751],
                            [-1.6456303432964996, 52.37595650500795],
                            [-1.6387809762869334, 52.37465019373085],
                            [-1.634791788997145, 52.37389176044164],
                            [-1.6315921288927824, 52.37535622518402],
                            [-1.626696153184927, 52.377624376547374],
                            [-1.623333981654566, 52.379133055316025],
                            [-1.6197350635873287, 52.380811690549756],
                            [-1.6161362623497628, 52.382445265672246],
                            [-1.61410115397588, 52.3850098287682]],
                    "type": "LineString"
                },
                "srid": 4326
            }
        """

        data = json.loads(json_payload)
        serializer = OverheadLineSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        serializer.save()
        self.assertEqual(OverheadLine.objects.count(), 1)


class TestSchoolSerializer(TestCase):
    @pytest.mark.django_db
    def test_school_serializer_create_object(self):
        json_payload = """
            {
                "urn": "100000",
                "la_name": "School Sample",
                "school_name": "School",
                "school_type": "Primary",
                "school_capacity": "300",
                "school_pupils": "280",
                "postcode": "EC3A 5DE",
                "point": {
                    "type": "Point",
                    "coordinates": [533498, 181201]
                },
                "srid": 27700
            }
        """

        data = json.loads(json_payload)
        serializer = SchoolSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        serializer.save()
        self.assertEqual(School.objects.count(), 1)
