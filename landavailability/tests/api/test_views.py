import json
from pprint import pprint

import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from api.models import (
    BusStop, TrainStop, Address, CodePoint, Broadband, MetroTube, Greenbelt,
    Motorway, Substation, OverheadLine, School, Location)
from api.serializers import (
    LocationSerializer, CodePointSerializer, BroadbandSerializer)


class LandAvailabilityAdminAPITestCase(APITestCase):
    @pytest.mark.django_db
    def setUp(self):
        self.user = User.objects.create_superuser(
            username='test', email='test@…', password='top_secret')
        token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)


class LandAvailabilityUserAPITestCase(APITestCase):
    @pytest.mark.django_db
    def setUp(self):
        self.user = User.objects.create_user(
            username='test', email='test@…', password='top_secret')
        token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)


class TestBusStopView(LandAvailabilityAdminAPITestCase):
    @pytest.mark.django_db
    def test_busstop_view_create_object(self):
        url = reverse('busstops-create')
        data = {
            "amic_code": "1800AMIC001",
            "point": {
                "type": "Point",
                "coordinates": [-2.347743000012108, 53.38737090322739]
            },
            "name": "Altrincham Interchange",
            "direction": "Nr Train Station",
            "area": "NA",
            "road": "STAMFORD NEW RD",
            "nptg_code": "E0028261",
            "srid": 4326
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BusStop.objects.count(), 1)

        response = self.client.post(url, data, format='json')
        self.assertEqual(BusStop.objects.count(), 1)


class TestTrainStopView(LandAvailabilityAdminAPITestCase):
    @pytest.mark.django_db
    def test_trainstop_view_create_object(self):
        url = reverse('trainstops-create')
        data = {
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

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TrainStop.objects.count(), 1)

        response = self.client.post(url, data, format='json')
        self.assertEqual(TrainStop.objects.count(), 1)


class TestAddressView(LandAvailabilityAdminAPITestCase):
    @pytest.mark.django_db
    def test_address_view_create_object(self):
        url = reverse('addresses-create')
        data = {
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

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Address.objects.count(), 1)

        response = self.client.post(url, data, format='json')
        self.assertEqual(Address.objects.count(), 1)


class TestCodePointView(LandAvailabilityAdminAPITestCase):
    @pytest.mark.django_db
    def test_codepoint_view_create_object(self):
        url = reverse('codepoints-create')
        data = {
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

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CodePoint.objects.count(), 1)

        response = self.client.post(url, data, format='json')
        self.assertEqual(CodePoint.objects.count(), 1)


class TestBroadbandView(LandAvailabilityAdminAPITestCase):
    @pytest.mark.django_db
    def test_broadband_view_create_object(self):
        # Prepare a CodePoint
        codepoint = CodePoint()
        codepoint.postcode = 'ME58TL'
        codepoint.point = Point(
            float("-1.83356713993623"), float("55.4168769443259"))
        codepoint.quality = 10
        codepoint.save()

        url = reverse('broadbands-create')
        data = {
            "postcode": "ME5 8TL",
            "speed_30_mb_percentage": 50,
            "avg_download_speed": 10.5,
            "min_download_speed": 2.8,
            "max_download_speed": 12.3,
            "avg_upload_speed": 0.5,
            "min_upload_speed": 0.3,
            "max_upload_speed": 1.1
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Broadband.objects.count(), 1)

        response = self.client.post(url, data, format='json')
        self.assertEqual(Broadband.objects.count(), 1)


class TestMetroTubeView(LandAvailabilityAdminAPITestCase):
    @pytest.mark.django_db
    def test_metrotube_view_create_object(self):
        url = reverse('metrotubes-create')
        data = {
            "atco_code": "1800AMIC001",
            "name": "Altrincham Interchange",
            "naptan_code": "bsstnxl",
            "locality": "",
            "point": {
                "type": "Point",
                "coordinates": [-2.347743000012108, 53.38737090322739]
            },
            "srid": 4326
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MetroTube.objects.count(), 1)

        response = self.client.post(url, data, format='json')
        self.assertEqual(MetroTube.objects.count(), 1)

    @pytest.mark.django_db
    def test_metrotube_view_create_object_no_naptan(self):
        url = reverse('metrotubes-create')
        data = {
            "atco_code": "1800AMIC001",
            "name": "Altrincham Interchange",
            "locality": "",
            "point": {
                "type": "Point",
                "coordinates": [-2.347743000012108, 53.38737090322739]
            },
            "srid": 4326
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MetroTube.objects.count(), 1)

        response = self.client.post(url, data, format='json')
        self.assertEqual(MetroTube.objects.count(), 1)

    @pytest.mark.django_db
    def test_metrotube_view_create_object_blank_naptan(self):
        url = reverse('metrotubes-create')
        data = {
            "atco_code": "1800AMIC001",
            "name": "Altrincham Interchange",
            "naptan_code": '',
            "locality": "",
            "point": {
                "type": "Point",
                "coordinates": [-2.347743000012108, 53.38737090322739]
            },
            "srid": 4326
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MetroTube.objects.count(), 1)

        response = self.client.post(url, data, format='json')
        self.assertEqual(MetroTube.objects.count(), 1)


class TestGreenbeltView(LandAvailabilityAdminAPITestCase):
    @pytest.mark.django_db
    def test_greenbelt_view_create_object(self):
        url = reverse('greenbelts-create')
        data = {
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

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Greenbelt.objects.count(), 1)

        response = self.client.post(url, data, format='json')
        self.assertEqual(Greenbelt.objects.count(), 1)


class TestMotorwayView(LandAvailabilityAdminAPITestCase):
    @pytest.mark.django_db
    def test_motorway_view_create_object(self):
        url = reverse('motorways-create')
        data = {
            "identifier": "1800AMIC001",
            "number": "M58",
            "point": {
                "type": "Point",
                "coordinates": [-2.347743000012108, 53.38737090322739]
            },
            "srid": 4326
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Motorway.objects.count(), 1)

        response = self.client.post(url, data, format='json')
        self.assertEqual(Motorway.objects.count(), 1)


class TestSubstationView(LandAvailabilityAdminAPITestCase):
    @pytest.mark.django_db
    def test_substation_view_create_object(self):
        url = reverse('substations-create')
        data = {
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

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Substation.objects.count(), 1)

        response = self.client.post(url, data, format='json')
        self.assertEqual(Substation.objects.count(), 1)


class TestOverheadLineView(LandAvailabilityAdminAPITestCase):
    @pytest.mark.django_db
    def test_overheadline_view_create_object(self):
        url = reverse('overheadlines-create')
        data = {
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

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(OverheadLine.objects.count(), 1)

        response = self.client.post(url, data, format='json')
        self.assertEqual(OverheadLine.objects.count(), 1)


class TestSchoolView(LandAvailabilityAdminAPITestCase):
    @pytest.mark.django_db
    def test_school_view_create_object(self):
        url = reverse('schools-create')
        data = {
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

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(School.objects.count(), 1)

        response = self.client.post(url, data, format='json')
        self.assertEqual(School.objects.count(), 1)


class TestLocationViewPost(LandAvailabilityAdminAPITestCase):
    @pytest.mark.django_db
    def test_location_create_view_create_object(self):
        url = reverse('locations')
        data = {
            "uprn": "123456789AB",
            "ba_ref": "47523471536",
            "name": "St James C E Secondary School (10910)",
            "authority": "Bolton",
            "owner": "Test owner",
            "unique_asset_id": "10910",
            "geom": {
                "type": "MultiPolygon",
                "coordinates": [
                    [
                        [
                            [
                                -2.1614837256814963,
                                53.07183331520438
                            ],
                            [
                                -2.161440204004493,
                                53.07167876512527
                            ],
                            [
                                -2.161426422046515,
                                53.07158231050548
                            ],
                            [
                                -2.161412261861244,
                                53.07128283205548
                            ],
                            [
                                -2.161373377871479,
                                53.071211109880664
                            ],
                            [
                                -2.161369504865456,
                                53.07118401041043
                            ],
                            [
                                -2.1617677327485008,
                                53.07111245525075
                            ],
                            [
                                -2.1617682739467705,
                                53.071109120469266
                            ],
                            [
                                -2.1620568237599738,
                                53.07147709017702
                            ],
                            [
                                -2.162246918923053,
                                53.07170561414385
                            ],
                            [
                                -2.162193868651531,
                                53.07171503969784
                            ],
                            [
                                -2.162142294698858,
                                53.07172373689699
                            ],
                            [
                                -2.1621361236605248,
                                53.07171871503741
                            ],
                            [
                                -2.1614837256814963,
                                53.07183331520438
                            ]
                        ]
                    ]
                ]
            },
            "srid": 4326
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Location.objects.count(), 1)

        response = self.client.post(url, data, format='json')
        self.assertEqual(Location.objects.count(), 1)


class TestLocationViewGet(LandAvailabilityUserAPITestCase):
    @pytest.mark.django_db
    def test_location_view_get_locations(self):
        # Create test CodePoint

        json_payload = """{
                "postcode": "CB11AZ",
                "quality": "10",
                "country": "E92000001",
                "nhs_region": "E19000001",
                "nhs_health_authority": "E18000002",
                "county": "",
                "district": "E08000002",
                "ward": "E05000681",
                "point": {
                    "type": "Point",
                    "coordinates": [0.13088953859958197, 52.20513657706537]
                },
                "srid": 4326
            }"""

        data = json.loads(json_payload)
        serializer = CodePointSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        serializer.save()

        # Create test Locations

        json_payload = """{
            "uprn": "010090969113",
            "ba_ref": "00004870000113",
            "name": "Test Location 1",
            "authority": "Cambridge City Council",
            "owner": "",
            "unique_asset_id": "",
            "geom": {
                "type": "MultiPolygon",
                "coordinates": [
                    [
                        [
                            [0.13153553009033203, 52.205765731674575],
                            [0.13143360614776609, 52.20569340742784],
                            [0.13174474239349365, 52.20561122064091],
                            [0.13180643320083618, 52.20569669489615],
                            [0.13153553009033203, 52.205765731674575]
                        ]
                    ]
                ]
            },
            "srid": 4326
        }"""

        data = json.loads(json_payload)
        serializer = LocationSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        serializer.save()

        json_payload = """{
            "uprn": "200004166552",
            "ba_ref": "00004310025025",
            "name": "Test Location 2",
            "authority": "Cambridge City Council",
            "owner": "",
            "unique_asset_id": "",
            "geom": {
                "type": "MultiPolygon",
                "coordinates": [
                    [
                        [
                            [0.13197273015975952, 52.20564902658178],
                            [0.13188958168029785, 52.20554218362242],
                            [0.13214707374572754, 52.205476433981275],
                            [0.13222217559814453, 52.205583277098725],
                            [0.13197273015975952, 52.20564902658178]
                        ]
                    ]
                ]
            },
            "srid": 4326
        }"""

        data = json.loads(json_payload)
        serializer = LocationSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        serializer.save()

        json_payload = """{
            "uprn": "200004178088",
            "ba_ref": "00006230135008",
            "name": "Test Location 3",
            "authority": "Cambridge City Council",
            "owner": "",
            "unique_asset_id": "",
            "geom": {
                "type": "MultiPolygon",
                "coordinates": [
                    [
                        [
                            [0.13076573610305786, 52.20487153271788],
                            [0.13069331645965576, 52.20480906961836],
                            [0.13091862201690674, 52.204717018574804],
                            [0.13101786375045776, 52.20480906961836],
                            [0.13076573610305786, 52.20487153271788]
                        ]
                    ]
                ]
            },
            "srid": 4326
        }"""

        data = json.loads(json_payload)
        serializer = LocationSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        serializer.save()

        # Get the data from the API
        url = reverse('locations')
        response = self.client.get(
            url, {'postcode': 'CB11AZ', 'range_distance': 1000})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 3)

    @pytest.mark.django_db
    def test_location_view_get_locations_selected_area(self):
        # Create test Locations

        json_payload = """{
            "uprn": "010090969113",
            "ba_ref": "00004870000113",
            "name": "Test Location 1",
            "authority": "Cambridge City Council",
            "owner": "",
            "unique_asset_id": "",
            "geom": {
                "type": "MultiPolygon",
                "coordinates": [
                    [
                        [
                            [0.13153553009033203, 52.205765731674575],
                            [0.13143360614776609, 52.20569340742784],
                            [0.13174474239349365, 52.20561122064091],
                            [0.13180643320083618, 52.20569669489615],
                            [0.13153553009033203, 52.205765731674575]
                        ]
                    ]
                ]
            },
            "srid": 4326
        }"""

        data = json.loads(json_payload)
        serializer = LocationSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        serializer.save()

        json_payload = """{
            "uprn": "200004166552",
            "ba_ref": "00004310025025",
            "name": "Test Location 2",
            "authority": "Cambridge City Council",
            "owner": "",
            "unique_asset_id": "",
            "geom": {
                "type": "MultiPolygon",
                "coordinates": [
                    [
                        [
                            [0.13197273015975952, 52.20564902658178],
                            [0.13188958168029785, 52.20554218362242],
                            [0.13214707374572754, 52.205476433981275],
                            [0.13222217559814453, 52.205583277098725],
                            [0.13197273015975952, 52.20564902658178]
                        ]
                    ]
                ]
            },
            "srid": 4326
        }"""

        data = json.loads(json_payload)
        serializer = LocationSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        serializer.save()

        # Get the data from the API
        url = reverse('locations')
        response = self.client.get(
            url, {
                'polygon': """[
                    [
                        [
                            0.0858306884765625,
                            52.18308960259887
                        ],
                        [
                            0.1786994934082031,
                            52.18308960259887
                        ],
                        [
                            0.1786994934082031,
                            52.22485521518378
                        ],
                        [
                            0.0858306884765625,
                            52.22485521518378
                        ],
                        [
                            0.0858306884765625,
                            52.18308960259887
                        ]
                    ]
                ]"""
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)

    @pytest.mark.django_db
    def test_location_view_get_no_locations_outside_selected_area(self):
        # Create test Locations

        json_payload = """{
            "uprn": "010090969113",
            "ba_ref": "00004870000113",
            "name": "Test Location 1",
            "authority": "Cambridge City Council",
            "owner": "",
            "unique_asset_id": "",
            "geom": {
                "type": "MultiPolygon",
                "coordinates": [
                    [
                        [
                            [0.13153553009033203, 52.205765731674575],
                            [0.13143360614776609, 52.20569340742784],
                            [0.13174474239349365, 52.20561122064091],
                            [0.13180643320083618, 52.20569669489615],
                            [0.13153553009033203, 52.205765731674575]
                        ]
                    ]
                ]
            },
            "srid": 4326
        }"""

        data = json.loads(json_payload)
        serializer = LocationSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        serializer.save()

        json_payload = """{
            "uprn": "200004166552",
            "ba_ref": "00004310025025",
            "name": "Test Location 2",
            "authority": "Cambridge City Council",
            "owner": "",
            "unique_asset_id": "",
            "geom": {
                "type": "MultiPolygon",
                "coordinates": [
                    [
                        [
                            [0.13197273015975952, 52.20564902658178],
                            [0.13188958168029785, 52.20554218362242],
                            [0.13214707374572754, 52.205476433981275],
                            [0.13222217559814453, 52.205583277098725],
                            [0.13197273015975952, 52.20564902658178]
                        ]
                    ]
                ]
            },
            "srid": 4326
        }"""

        data = json.loads(json_payload)
        serializer = LocationSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        serializer.save()

        # Get the data from the API
        url = reverse('locations')
        response = self.client.get(
            url, {
                'polygon': """[
                    [
                        [
                            0.05046844482421874,
                            52.3130964236375
                        ],
                        [
                            0.142822265625,
                            52.3130964236375
                        ],
                        [
                            0.142822265625,
                            52.343100382549984
                        ],
                        [
                            0.05046844482421874,
                            52.343100382549984
                        ],
                        [
                            0.05046844482421874,
                            52.3130964236375
                        ]
                    ]
                ]"""
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 0)

    @pytest.mark.django_db
    def test_location_view_get_locations_no_params(self):
        url = reverse('locations')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @pytest.mark.django_db
    def test_location_view_get_locations_invalid_postcode(self):
        url = reverse('locations')
        response = self.client.get(
            url, {'postcode': 'XX11YY', 'range_distance': 1000})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestLocationDetailsView(LandAvailabilityUserAPITestCase):
    @pytest.mark.django_db
    def test_location_details(self):
        # Create test Location

        json_payload = """{
            "uprn": "010090969113",
            "ba_ref": "00004870000113",
            "name": "Test Location 1",
            "authority": "Cambridge City Council",
            "owner": "",
            "unique_asset_id": "",
            "geom": {
                "type": "MultiPolygon",
                "coordinates": [
                    [
                        [
                            [0.13153553009033203, 52.205765731674575],
                            [0.13143360614776609, 52.20569340742784],
                            [0.13174474239349365, 52.20561122064091],
                            [0.13180643320083618, 52.20569669489615],
                            [0.13153553009033203, 52.205765731674575]
                        ]
                    ]
                ]
            },
            "srid": 4326
        }"""

        data = json.loads(json_payload)
        serializer = LocationSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        serializer.save()

        url = reverse('location-details', kwargs={'uprn': '010090969113'})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['uprn'], '010090969113')

    @pytest.mark.django_db
    def test_location_details_has_broadband(self):
        # Create test CodePoint

        json_payload = """{
                "postcode": "CB11AZ",
                "quality": "10",
                "country": "E92000001",
                "nhs_region": "E19000001",
                "nhs_health_authority": "E18000002",
                "county": "",
                "district": "E08000002",
                "ward": "E05000681",
                "point": {
                    "type": "Point",
                    "coordinates": [0.13088953859958197, 52.20513657706537]
                },
                "srid": 4326
            }"""

        data = json.loads(json_payload)
        serializer = CodePointSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        serializer.save()

        # Create test Broadband

        json_payload = """{
            "postcode": "CB11AZ",
            "speed_30_mb_percentage": 50,
            "avg_download_speed": 10.5,
            "min_download_speed": 2.8,
            "max_download_speed": 12.3,
            "avg_upload_speed": 0.5,
            "min_upload_speed": 0.3,
            "max_upload_speed": 1.1
        }"""

        data = json.loads(json_payload)
        serializer = BroadbandSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        serializer.save()

        # Create test Locations

        json_payload = """{
            "uprn": "010090969113",
            "ba_ref": "00004870000113",
            "name": "Test Location 1",
            "authority": "Cambridge City Council",
            "owner": "",
            "unique_asset_id": "",
            "geom": {
                "type": "MultiPolygon",
                "coordinates": [
                    [
                        [
                            [0.13153553009033203, 52.205765731674575],
                            [0.13143360614776609, 52.20569340742784],
                            [0.13174474239349365, 52.20561122064091],
                            [0.13180643320083618, 52.20569669489615],
                            [0.13153553009033203, 52.205765731674575]
                        ]
                    ]
                ]
            },
            "srid": 4326
        }"""

        data = json.loads(json_payload)
        serializer = LocationSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        serializer.save()

        url = reverse('location-details', kwargs={'uprn': '010090969113'})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['uprn'], '010090969113')
        self.assertEqual(response.json()['nearest_broadband_fast'], True)


FIXTURE_CODEPOINT_CB11AZ = {
    "postcode": "CB11AZ",
    "quality": "10",
    "country": "E92000001",
    "nhs_region": "E19000001",
    "nhs_health_authority": "E18000002",
    "county": "",
    "district": "E08000002",
    "ward": "E05000681",
    "point": {
        "type": "Point",
        "coordinates": [0.13088953859958197, 52.20513657706537]
    },
    "srid": 4326
}

FIXTURE_LOCATION_1 = {
    "uprn": "010090969113",
    "ba_ref": "00004870000113",
    "name": "Test Location 1",
    "authority": "Cambridge City Council",
    "owner": "",
    "unique_asset_id": "",
    "geom": {
        "type": "MultiPolygon",
        "coordinates": [
            [
                [
                    [0.13153553009033203, 52.205765731674575],
                    [0.13143360614776609, 52.20569340742784],
                    [0.13174474239349365, 52.20561122064091],
                    [0.13180643320083618, 52.20569669489615],
                    [0.13153553009033203, 52.205765731674575]
                ]
            ]
        ]
    },
    "srid": 4326
}

FIXTURE_LOCATION_2 = {
    "uprn": "200004166552",
    "ba_ref": "00004310025025",
    "name": "Test Location 2",
    "authority": "Cambridge City Council",
    "owner": "",
    "unique_asset_id": "",
    "geom": {
        "type": "MultiPolygon",
        "coordinates": [
            [
                [
                    [0.13197273015975952, 52.20564902658178],
                    [0.13188958168029785, 52.20554218362242],
                    [0.13214707374572754, 52.205476433981275],
                    [0.13222217559814453, 52.205583277098725],
                    [0.13197273015975952, 52.20564902658178]
                ]
            ]
        ]
    },
    "srid": 4326
}

FIXTURE_LOCATION_3 = {
    "uprn": "200004178088",
    "ba_ref": "00006230135008",
    "name": "Test Location 3",
    "authority": "Cambridge City Council",
    "owner": "",
    "unique_asset_id": "",
    "geom": {
        "type": "MultiPolygon",
        "coordinates": [
            [
                [
                    [0.13076573610305786, 52.20487153271788],
                    [0.13069331645965576, 52.20480906961836],
                    [0.13091862201690674, 52.204717018574804],
                    [0.13101786375045776, 52.20480906961836],
                    [0.13076573610305786, 52.20487153271788]
                ]
            ]
        ]
        },
    "srid": 4326
    }

POLYGON_CAMBRIDGE = {
    'polygon': """[
        [
            [
                0.0858306884765625,
                52.18308960259887
            ],
            [
                0.1786994934082031,
                52.18308960259887
            ],
            [
                0.1786994934082031,
                52.22485521518378
            ],
            [
                0.0858306884765625,
                52.22485521518378
            ],
            [
                0.0858306884765625,
                52.18308960259887
            ]
        ]
    ]"""
}

FIXTURE_BUS_STOP_CAMBRIDGE = (0.13076573610305786, 52.20487153271788)

class TestLocationSearch(LandAvailabilityUserAPITestCase):
    @pytest.mark.django_db
    def test_by_postcode(self):
        # Create test CodePoint
        serializer = CodePointSerializer(data=FIXTURE_CODEPOINT_CB11AZ)
        self.assertTrue(serializer.is_valid())
        serializer.save()

        # Create test Locations
        serializer = LocationSerializer(data=FIXTURE_LOCATION_1)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        serializer = LocationSerializer(data=FIXTURE_LOCATION_2)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        serializer = LocationSerializer(data=FIXTURE_LOCATION_3)
        self.assertTrue(serializer.is_valid())
        serializer.save()

        # Get the data from the API
        url = reverse('location-search')
        response = self.client.get(
            url, {'postcode': 'CB11AZ', 'range_distance': 1000})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 3)

    @pytest.mark.django_db
    def test_by_polygon(self):
        # Create test Locations
        serializer = LocationSerializer(data=FIXTURE_LOCATION_1)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        serializer = LocationSerializer(data=FIXTURE_LOCATION_2)
        self.assertTrue(serializer.is_valid())
        serializer.save()

        # Get the data from the API
        url = reverse('location-search')
        response = self.client.get(
            url, POLYGON_CAMBRIDGE,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)

    @pytest.mark.django_db
    def test_no_locations_outside_selected_area(self):
        # Create test Locations
        serializer = LocationSerializer(data=FIXTURE_LOCATION_1)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        serializer = LocationSerializer(data=FIXTURE_LOCATION_2)
        self.assertTrue(serializer.is_valid())
        serializer.save()

        # Get the data from the API
        url = reverse('location-search')
        response = self.client.get(
            url, {
                'polygon': """[
                    [
                        [
                            0.05046844482421874,
                            52.3130964236375
                        ],
                        [
                            0.142822265625,
                            52.3130964236375
                        ],
                        [
                            0.142822265625,
                            52.343100382549984
                        ],
                        [
                            0.05046844482421874,
                            52.343100382549984
                        ],
                        [
                            0.05046844482421874,
                            52.3130964236375
                        ]
                    ]
                ]"""
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 0)

    @pytest.mark.django_db
    def test_location_view_get_locations_no_params(self):
        url = reverse('location-search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @pytest.mark.django_db
    def test_location_view_get_locations_invalid_postcode(self):
        url = reverse('location-search')
        response = self.client.get(
            url, {'postcode': 'XX11YY', 'range_distance': 1000})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @pytest.mark.django_db
    def test_ranking(self):
        # Create test Locations
        serializer = LocationSerializer(data=FIXTURE_LOCATION_1)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        serializer = LocationSerializer(data=FIXTURE_LOCATION_2)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        serializer = LocationSerializer(data=FIXTURE_LOCATION_3)
        self.assertTrue(serializer.is_valid())
        serializer.save()

        # Add a bus stop so ranking has something to work on
        busstop = BusStop(name='Test Bus Stop',
                          point=Point(*FIXTURE_BUS_STOP_CAMBRIDGE))
        busstop.save()
        busstop.update_close_locations(default_range=3000)

        # Get the data from the API
        url = reverse('location-search')
        response = self.client.get(
            url, dict(POLYGON_CAMBRIDGE.items(),
                      build='secondary_school'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        pprint(response.json())
        self.assertEqual(len(response.json()), 3)
        self.assertEqual(response.json()[0]['name'], 'Test Location 3')

    @pytest.mark.django_db
    def test_ranking_no_pupils_param(self):
        url = reverse('location-search')
        response = self.client.get(url, build='secondary_school')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @pytest.mark.django_db
    def test_ranking_non_int_page_size(self):
        url = reverse('location-search')
        response = self.client.get(url, page_size='string')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @pytest.mark.django_db
    def test_ranking_negative_page_size(self):
        url = reverse('location-search')
        response = self.client.get(url, page_size=-5)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @pytest.mark.django_db
    def test_ranking_page_size_too_big(self):
        url = reverse('location-search')
        response = self.client.get(url, page_size=1e6)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @pytest.mark.django_db
    def test_ranking_non_int_page(self):
        url = reverse('location-search')
        response = self.client.get(url, page='string')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @pytest.mark.django_db
    def test_ranking_negative_page(self):
        url = reverse('location-search')
        response = self.client.get(url, page=-5)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @pytest.mark.django_db
    def test_ranking_page_too_big(self):
        url = reverse('location-search')
        response = self.client.get(url, page=1e6)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
