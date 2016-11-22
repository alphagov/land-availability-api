from django.contrib.gis.db import models


class Address(models.Model):
    # Describes an instance of an address

    uprn = models.CharField(db_index=True, max_length=100)
    address_line_1 = models.CharField(max_length=255, blank=True, null=True)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    address_line_3 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    county = models.CharField(max_length=255, blank=True, null=True)
    postcode = models.CharField(max_length=50, blank=True, null=True)
    country_code = models.CharField(max_length=50, blank=True, null=True)
    point = models.PointField()


class CodePoint(models.Model):
    # Describes an instance of a Code Point

    postcode = models.CharField(db_index=True, max_length=20)
    quality = models.IntegerField()
    point = models.PointField()
    country = models.CharField(db_index=True, max_length=24)
    nhs_region = models.CharField(db_index=True, max_length=24)
    nhs_health_authority = models.CharField(db_index=True, max_length=24)
    county = models.CharField(db_index=True, max_length=24)
    district = models.CharField(db_index=True, max_length=24)
    ward = models.CharField(db_index=True, max_length=24)
