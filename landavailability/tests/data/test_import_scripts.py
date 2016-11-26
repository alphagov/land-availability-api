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
from api.models import Address, BusStop, CodePoint, TrainStop
from django.contrib.gis.geos import Point


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
