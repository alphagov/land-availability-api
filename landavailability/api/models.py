from django.contrib.gis.db import models
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from django.db.models.signals import pre_delete
from django.dispatch import receiver


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

    def update_close_locations(self, default_range=1000):
        locations = Location.objects.filter(
            geom__dwithin=(self.point, D(m=default_range))).\
            annotate(distance=Distance('geom', self.point))

        for location in locations:
            if location.nearest_busstop:
                if location.distance.m > location.nearest_busstop_distance:
                    continue

            location.nearest_busstop = self
            location.nearest_busstop_distance = location.distance.m
            location.save()


@receiver(pre_delete, sender=BusStop, weak=False)
def busstop_predelete_handler(sender, instance, **kwargs):
    """
    Whenever we try to delete a BusStop, we search all the Locations using it
    and we remove the reference, so the object can be safely deleted.
    """
    Location.objects.filter(nearest_busstop__id=instance.id).\
        update(nearest_busstop=None, nearest_busstop_distance=0)


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

    def update_close_locations(self, default_range=1000):
        locations = Location.objects.filter(
            geom__dwithin=(self.point, D(m=default_range))).\
            annotate(distance=Distance('geom', self.point))

        for location in locations:
            if location.nearest_trainstop:
                if location.distance.m > location.nearest_trainstop_distance:
                    continue

            location.nearest_trainstop = self
            location.nearest_trainstop_distance = location.distance.m
            location.save()


@receiver(pre_delete, sender=TrainStop, weak=False)
def trainstop_predelete_handler(sender, instance, **kwargs):
    """
    Whenever we try to delete a TrainStop, we search all the Locations using it
    and we remove the reference, so the object can be safely deleted.
    """
    Location.objects.filter(nearest_trainstop__id=instance.id).\
        update(nearest_trainstop=None, nearest_trainstop_distance=0)


class Location(models.Model):
    # Describes an instance of a Location

    name = models.CharField(db_index=True, max_length=255)
    point = models.PointField(geography=True, spatial_index=True)
    geom = models.MultiPolygonField(geography=True, spatial_index=True)
    authority = models.CharField(max_length=255, blank=True, null=True)
    owner = models.CharField(max_length=255, blank=True, null=True)
    uprn = models.CharField(max_length=100, blank=True, null=True)
    unique_asset_id = models.CharField(max_length=100, blank=True, null=True)
    nearest_busstop = models.ForeignKey(
        BusStop, on_delete=models.SET_NULL, null=True)
    nearest_busstop_distance = models.FloatField(null=True)  # meters
    nearest_trainstop = models.ForeignKey(
        TrainStop, on_delete=models.SET_NULL, null=True)
    nearest_trainstop_distance = models.FloatField(null=True)  # meters

    def update_nearest_busstop(self, distance=1000):
        bss = BusStop.objects.filter(
            point__dwithin=(self.geom, D(m=distance))).annotate(
            distance=Distance('point', self.geom)).order_by('distance')

        if len(bss) > 0:
            self.nearest_busstop = bss[0]
            self.nearest_busstop_distance = bss[0].distance.m

    def update_nearest_trainstop(self, distance=1000):
        tss = TrainStop.objects.filter(
            point__dwithin=(self.geom, D(m=distance))).annotate(
            distance=Distance('point', self.geom)).order_by('distance')

        if len(tss) > 0:
            self.nearest_trainstop = tss[0]
            self.nearest_trainstop_distance = tss[0].distance.m

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.update_nearest_busstop()
            self.update_nearest_trainstop()

        super(Location, self).save(*args, **kwargs)
