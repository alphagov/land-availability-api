from unittest import TestCase
import pytest
from api.management.commands.import_addresses import (
    Command as AddressesCommand,
)
from api.management.commands.import_busstops import (
    Command as BusStopCommand,
)
from api.models import Address, BusStop
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
        self.assertEqual(
            bus_stop.point,
            Point(
                float("-2.347743000012108"),
                float("53.38737090322739")))
        self.assertEqual(bus_stop.name, 'Honolulu Interchange')
        self.assertEqual(bus_stop.direction, 'Nr Train Station')
        self.assertEqual(bus_stop.area, 'NA')
        self.assertEqual(bus_stop.road, 'HONOLULU NEW RD')
        self.assertEqual(bus_stop.nptg_code, 'A00223344')
