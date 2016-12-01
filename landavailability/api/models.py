from django.contrib.gis.db import models
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D


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
    point = models.PointField(geography=True, spatial_index=True)


class CodePoint(models.Model):
    # Describes an instance of a Code Point

    postcode = models.CharField(db_index=True, max_length=20)
    quality = models.IntegerField()
    point = models.PointField(geography=True, spatial_index=True)
    country = models.CharField(db_index=True, max_length=24)
    nhs_region = models.CharField(db_index=True, max_length=24)
    nhs_health_authority = models.CharField(db_index=True, max_length=24)
    county = models.CharField(db_index=True, max_length=24)
    district = models.CharField(db_index=True, max_length=24)
    ward = models.CharField(db_index=True, max_length=24)


class BusStop(models.Model):
    # Describes an instance of a bus stop

    amic_code = models.CharField(db_index=True, max_length=20)
    point = models.PointField(geography=True, spatial_index=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    direction = models.CharField(max_length=255, blank=True, null=True)
    area = models.CharField(max_length=20, blank=True, null=True)
    road = models.CharField(max_length=255, blank=True, null=True)
    nptg_code = models.CharField(max_length=255, blank=True, null=True)

    def update_close_locations(self, distance=1000):
        locations = Location.objects.filter(
            geom__dwithin=(self.point, D(m=distance)))

        for location in locations:
            distance = location.geom.distance(self.point)

            if location.nearest_busstop:
                if distance > location.geom.distance(
                        location.nearest_busstop.point):
                    continue

            location.nearest_busstop = self
            # FIXME: distance is espressed in a linear way
            # location.nearest_busstop_distance = distance
            location.save()


class TrainStop(models.Model):
    # Describes an instance of a train stop

    atcode_code = models.CharField(db_index=True, max_length=24)
    naptan_code = models.CharField(max_length=24, blank=True, null=True)
    point = models.PointField(geography=True, spatial_index=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    main_road = models.CharField(max_length=255, blank=True, null=True)
    side_road = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=24, blank=True, null=True)
    nptg_code = models.CharField(max_length=255, blank=True, null=True)
    local_reference = models.CharField(max_length=255, blank=True, null=True)


class Location(models.Model):
    # Describes an instance of a Location

    name = models.CharField(db_index=True, max_length=255)
    point = models.PointField(geography=True, spatial_index=True)
    geom = models.MultiPolygonField(geography=True, spatial_index=True)
    authority = models.CharField(max_length=255, blank=True, null=True)
    owner = models.CharField(max_length=255, blank=True, null=True)
    uprn = models.CharField(max_length=100, blank=True, null=True)
    unique_asset_id = models.CharField(max_length=100, blank=True, null=True)
    nearest_busstop = models.ForeignKey(BusStop, null=True)
    nearest_busstop_distance = models.FloatField(null=True)  # meters
    nearest_trainstop = models.ForeignKey(TrainStop, null=True)
    nearest_trainstop_distance = models.FloatField(null=True)  # meters

    def refresh_busstop_distance(self):
        if self.nearest_busstop:
            distance = Location.objects.filter(id=self.id).\
                annotate(
                    distance=Distance('geom', self.nearest_busstop.point))[0].\
                distance.m
            self.nearest_busstop_distance = distance
            self.save()
