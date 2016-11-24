from unittest import TestCase
import pytest
from api.management.commands.import_addresses import (
    Command as AddressesCommand
)
from api.models import Address


class TestAddressCommand(TestCase):
    @pytest.mark.django_db
    def test_import_addresses_process_row(self):
        address_row = [
            "3225845", "10091033016", "Bolton Chapel",
            "Bolton Village Main Street", "", "Bolton", "Northumberland",
            "NE66 2EE", "GB", "55.4168769443259", "-1.83356713993623"]

        AddressesCommand().process_row(address_row)
        self.assertEqual(Address.objects.count(), 1)
