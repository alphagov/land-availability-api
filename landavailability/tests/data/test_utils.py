from unittest import TestCase
import pytest
from api.models import Address, CodePoint
from api.management.commands.utils import (
    get_address_from_postcode, get_codepoint_from_postcode)
from django.contrib.gis.geos import Point


class TestUtils(TestCase):
    @pytest.mark.django_db
    def test_get_address_from_postcode_single(self):
        address = Address()
        address.uprn = "123456"
        address.address_line_1 = "Dataland Village Main Street"
        address.postcode = "AA111ZZ"
        address.point = Point(
            float("-1.83356713993623"),
            float("55.4168769443259"),
            srid=4326)
        address.save()

        found_address = get_address_from_postcode('AA111ZZ')

        self.assertIsNotNone(found_address)
        self.assertEqual(found_address[0].uprn, '123456')

    @pytest.mark.django_db
    def test_get_address_from_postcode_none(self):
        found_address = get_address_from_postcode('AA111ZZ')

        self.assertEqual(len(found_address), 0)

    @pytest.mark.django_db
    def test_get_codepoint_from_postcode_single(self):
        codepoint = CodePoint()
        codepoint.postcode = 'AA111ZZ'
        codepoint.quality = 10
        codepoint.point = Point(
            float("-1.83356713993623"),
            float("55.4168769443259"),
            srid=4326)
        codepoint.country = 'E92000001'
        codepoint.nhs_region = 'E19000001'
        codepoint.nhs_health_authority = 'E18000002'
        codepoint.county = ''
        codepoint.district = 'E08000002'
        codepoint.ward = 'E05000681'
        codepoint.save()

        found_codepoint = get_codepoint_from_postcode('AA111ZZ')

        self.assertIsNotNone(found_codepoint)
        self.assertEqual(found_codepoint.postcode, 'AA111ZZ')

    @pytest.mark.django_db
    def test_get_codepoint_from_postcode_none(self):
        found_codepoint = get_codepoint_from_postcode('AA111ZZ')
        self.assertIsNone(found_codepoint)
