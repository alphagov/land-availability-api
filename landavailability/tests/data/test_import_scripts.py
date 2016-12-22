from unittest import TestCase
import pytest
from api.management.commands.import_addresses import (
    Command as AddressesCommand,
)
from api.management.commands.import_busstops import (
    Command as BusStopCommand,
)
from api.management.commands.import_codepoints import (
    Command as CodePointCommand,
)
from api.management.commands.import_trains import (
    Command as TrainStopCommand,
)
from api.management.commands.import_manchester_lands import (
    Command as ManchesterLandsCommand,
)
from api.management.commands.import_broadband import (
    Command as BroadbandCommand,
)
from api.management.commands.import_greenbelts import (
    Command as GreenbeltCommand,
)
from api.management.commands.import_schools import (
    Command as SchoolCommand,
)
from api.management.commands.import_metrotube import (
    Command as MetroTubeCommand,
)
from api.models import (
    Address, BusStop, CodePoint, TrainStop, Location, Broadband, Greenbelt,
    School, MetroTube)
from django.contrib.gis.geos import Point
import json


class TestAddressCommand(TestCase):
    @pytest.mark.django_db
    def test_import_addresses_process_row(self):
        address_row = [
            "123456", "273548175", "Dataland",
            "Dataland Village Main Street", "", "Dataland City",
            "Cucumberland", "AA11 1ZZ", "GB", "55.4168769443259",
            "-1.83356713993623"]

        AddressesCommand().process_row(address_row)
        self.assertEqual(Address.objects.count(), 1)

        address = Address.objects.first()
        self.assertEqual(address.uprn, '123456')
        self.assertEqual(address.address_line_1, 'Dataland')
        self.assertEqual(address.address_line_2, 'Dataland Village Main Street')
        self.assertEqual(address.address_line_3, '')
        self.assertEqual(address.city, 'Dataland City')
        self.assertEqual(address.county, 'Cucumberland')
        self.assertEqual(address.postcode, 'AA111ZZ')
        self.assertEqual(address.country_code, 'GB')
        self.assertEqual(
            address.point,
            Point(
                float("-1.83356713993623"),
                float("55.4168769443259")))


class TestBusStopCommand(TestCase):
    @pytest.mark.django_db
    def test_import_bus_stop_process_row(self):
        bus_stop_row = [
            "1800AMIC001", "", "376969", "387893",
            "Honolulu Interchange", "Nr Train Station", "NA",
            "HONOLULU NEW RD", "Honolulu Interchange", "A00223344", "", "",
            "BCS", "MKD", "TIP", "ACT", "17", "STOP BB REMOVED FROM AMIC",
            "Y", "MANADADG", "Interchange", "2014-12-18"]

        BusStopCommand().process_row(bus_stop_row)
        self.assertEqual(BusStop.objects.count(), 1)

        bus_stop = BusStop.objects.first()
        self.assertEqual(bus_stop.amic_code, '1800AMIC001')
        self.assertEqual(bus_stop.name, 'Honolulu Interchange')
        self.assertEqual(bus_stop.direction, 'Nr Train Station')
        self.assertEqual(bus_stop.area, 'NA')
        self.assertEqual(bus_stop.road, 'HONOLULU NEW RD')
        self.assertEqual(bus_stop.nptg_code, 'A00223344')


class TestCodePointCommand(TestCase):
    @pytest.mark.django_db
    def test_import_codepoint_process_row(self):
        codepoint_row = [
            "BL0 0AA", "10", "379448", "416851", "E92000001", "E19000001",
            "E18000002", "", "E08000002", "E05000681"]

        CodePointCommand().process_row(codepoint_row)
        self.assertEqual(CodePoint.objects.count(), 1)

        codepoint = CodePoint.objects.first()
        self.assertEqual(codepoint.postcode, 'BL00AA')
        self.assertEqual(codepoint.quality, 10)
        self.assertEqual(codepoint.country, 'E92000001')
        self.assertEqual(codepoint.nhs_region, 'E19000001')
        self.assertEqual(codepoint.nhs_health_authority, 'E18000002')
        self.assertEqual(codepoint.county, '')
        self.assertEqual(codepoint.district, 'E08000002')
        self.assertEqual(codepoint.ward, 'E05000681')


class TestTrainStopCommand(TestCase):
    @pytest.mark.django_db
    def test_import_train_stop_process_row(self):
        train_stop_row = [
            '9100ALTRNHM', '', '377008', '387924', 'DATALAND INTERCHANGE',
            'DATALAND NEW RD', 'DATA LANE', 'R', 'E0028261', 'AA123ZZ']

        TrainStopCommand().process_row(train_stop_row)
        self.assertEqual(TrainStop.objects.count(), 1)

        train_stop = TrainStop.objects.first()
        self.assertEqual(train_stop.atcode_code, '9100ALTRNHM')
        self.assertEqual(train_stop.naptan_code, '')
        self.assertEqual(train_stop.name, 'DATALAND INTERCHANGE')
        self.assertEqual(train_stop.main_road, 'DATALAND NEW RD')
        self.assertEqual(train_stop.side_road, 'DATA LANE')
        self.assertEqual(train_stop.type, 'R')
        self.assertEqual(train_stop.nptg_code, 'E0028261')
        self.assertEqual(train_stop.local_reference, 'AA123ZZ')


class TestManchesterLandCommand(TestCase):
    @pytest.mark.django_db
    def test_import_manchester_lands_process_feature(self):
        feature_json = """
            {
                "type": "Feature",
                "geometry_name": "wkb_geometry",
                "id": "v_gm_land_and_building_assets.fid-4118d472_152ea355a4",
                "properties": {
                    "unique_asset_id": "10910",
                    "holding_type": "Land and buildings",
                    "geom_type": "MULTIPOLYGON",
                    "tenure_detail": null,
                    "la": "Bolton",
                    "address": "St James C E Secondary School (10910)",
                    "temp_fid": "bol-2",
                    "tenure_type": "Leasehold ",
                    "other_detail": null
                },
                "geometry": {
                    "coordinates": [
                    [
                        [
                            [100.0, 0.0],
                            [101.0, 0.0],
                            [101.0, 1.0],
                            [100.0, 1.0],
                            [100.0, 0.0]
                        ]
                    ],
                    [
                        [
                            [100.0, 0.0],
                            [101.0, 0.0],
                            [101.0, 1.0],
                            [100.0, 1.0],
                            [100.0, 0.0]
                        ]
                    ]
                    ],
                    "type": "MultiPolygon"
                }
        }"""

        ManchesterLandsCommand().process_feature(json.loads(feature_json))
        self.assertEqual(Location.objects.count(), 1)


class TestBroadbandCommand(TestCase):
    @pytest.mark.django_db
    def test_import_broadband_process_row(self):
        codepoint = CodePoint()
        codepoint.postcode = 'ME58TL'
        codepoint.point = Point(
            float("-1.83356713993623"), float("55.4168769443259"))
        codepoint.quality = 10
        codepoint.country = 'E92000001'
        codepoint.nhs_region = 'E19000001'
        codepoint.nhs_health_authority = 'E18000002'
        codepoint.county = ''
        codepoint.district = 'E08000002'
        codepoint.ward = 'E05000681'
        codepoint.save()

        broadband_row = [
            'ME58TL', '100', '100', '2', '2', '1', '12', '49.1',
            '30', '0.9', '152', '63.3', '2.9', '67', '6.1', '4.7', '2', '0.6',
            '15', '5.8', '0.9', '6.2', '1.1']

        BroadbandCommand().process_row(broadband_row)
        self.assertEqual(Broadband.objects.count(), 1)

        broadband = Broadband.objects.first()
        self.assertEqual(broadband.postcode, 'ME58TL')
        self.assertEqual(broadband.speed_30_mb_percentage, 100.00)


class TestGreenbeltCommand(TestCase):
    @pytest.mark.django_db
    def test_import_greenbelt_process_feature(self):
        feature_json = """
        {
            "geometry": {
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
            "geometry_name": "the_geom",
            "id": "Local_Authority_green_belt_boundaries_2014-15.25",
            "type": "Feature",
            "properties": {
                "Shape_Area": 2888.41601134,
                "OBJECTID_1": 25,
                "OBJECTID": 25,
                "Shape_Le_1": 228.402024269,
                "LA_Name": "City of Stoke-on-Trent (B)",
                "ONS_CODE": "E06000021",
                "Year": "2014/15",
                "Area_Ha": 0.288841578377,
                "GB_name": "Stoke Greenbelt",
                "Perim_Km": 0.228402022276
            }
        }"""

        GreenbeltCommand().process_feature(json.loads(feature_json))
        self.assertEqual(Greenbelt.objects.count(), 1)


class TestSchoolCommand(TestCase):
    @pytest.mark.django_db
    def test_import_school_process_row(self):

        school_row = [
            "100000", "201", "City of London", "3614",
            "Sir John Cass's Foundation Primary School",
            "Voluntary Aided School", "Open", "Not applicable", "",
            "Not applicable", "", "Primary", "3", "11", "No Boarders",
            "Does not have a sixth form", "Mixed", "Church of England",
            "Diocese of London", "Not applicable", "210", "No Special Classes",
            "15-01-2015", "240", "125", "115", "21.5", "Not applicable", "",
            "Not applicable", "", "Not under a federation", "", "", "",
            "Not applicable", "18-04-2013", "Not in special measures",
            "24-09-2015", "St James's Passage", "Duke's Place", "", "London",
            "", "EC3A 5DE", "www.sirjohncassprimary.org", "02072831147",
            "Mr", "T", "Wilson", "", "Headteacher", "Not applicable", "",
            "Not applicable", "Not applicable", "Not applicable", "",
            "Not applicable", "Not applicable", "", "", "", "London", "Tower",
            "Cities of London and Westminster", "Urban major conurbation",
            "E09000001", "533498", "181201", "City of London 001",
            "City of London 001F", "", "999", "", ""]

        SchoolCommand().process_row(school_row)
        self.assertEqual(School.objects.count(), 1)

        school = School.objects.first()
        self.assertEqual(
            school.school_name, "Sir John Cass's Foundation Primary School")


class TestMetroTubeCommand(TestCase):
    @pytest.mark.django_db
    def test_import_metrotube_process_row(self):

        metrotube_row = [
            "0100BRP90207", "bstmdat", "", "", "Royate Hill", "en", "", "", "",
            "", "Fishponds Road", "en", "", "", "W-bound", "en", "W",
            "E0035600", "Eastville", "Bristol", "", "", "", "", "", "0", "U",
            "361854", "175047", "-2.5506067921", "51.4730930083", "TMU", "MKD",
            "OTH", "", "", "", "009", "2016-12-20T16:30:38",
            "2016-10-31T10:33:04", "4", "new", "act"]

        MetroTubeCommand().process_row(metrotube_row)
        self.assertEqual(MetroTube.objects.count(), 1)

        metrotube = MetroTube.objects.first()
        self.assertEqual(metrotube.atco_code, "0100BRP90207")
