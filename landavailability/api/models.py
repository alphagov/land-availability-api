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


class Substation(models.Model):
    # Describe an instance of a Substation

    name = models.CharField(db_index=True, max_length=255)
    operating = models.CharField(max_length=255, blank=True, null=True)
    action_dtt = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    owner_flag = models.CharField(max_length=255, blank=True, null=True)
    gdo_gid = models.CharField(max_length=255, blank=True, null=True)
    geom = models.PolygonField(geography=True, spatial_index=True)

    def update_close_locations(self, default_range=1000):
        locations = Location.objects.filter(
            geom__dwithin=(self.geom, D(m=default_range))).\
            annotate(distance=Distance('geom', self.geom))

        for location in locations:
            if location.nearest_substation:
                if location.distance.m > location.nearest_substation_distance:
                    continue

            location.nearest_substation = self
            location.nearest_substation_distance = location.distance.m
            location.save()


@receiver(pre_delete, sender=Substation, weak=False)
def substation_predelete_handler(sender, instance, **kwargs):
    """
    Whenever we try to delete a Substation, we search all the Locations using
    it and we remove the reference, so the object can be safely deleted.
    """
    Location.objects.filter(nearest_substation__id=instance.id).\
        update(nearest_substation=None, nearest_substation_distance=0)


class OverheadLine(models.Model):
    # Describe an instance of Overhead Line

    gdo_gid = models.CharField(db_index=True, max_length=255)
    route_asset = models.CharField(max_length=255, blank=True, null=True)
    towers = models.CharField(max_length=255, blank=True, null=True)
    action_dtt = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    operating = models.CharField(max_length=255, blank=True, null=True)
    circuit_1 = models.CharField(max_length=255, blank=True, null=True)
    circuit_2 = models.CharField(max_length=255, blank=True, null=True)
    geom = models.GeometryField(geography=True, spatial_index=True)

    def update_close_locations(self, default_range=1000):
        locations = Location.objects.filter(
            geom__dwithin=(self.geom, D(m=default_range))).\
            annotate(distance=Distance('geom', self.geom))

        for location in locations:
            if location.nearest_ohl:
                if location.distance.m > location.nearest_ohl_distance:
                    continue

            location.nearest_ohl = self
            location.nearest_ohl_distance = location.distance.m
            location.save()


@receiver(pre_delete, sender=OverheadLine, weak=False)
def overheadline_predelete_handler(sender, instance, **kwargs):
    """
    Whenever we try to delete an Overhead Line, we search all the Locations
    using it and we remove the reference, so the object can be safely deleted.
    """
    Location.objects.filter(nearest_ohl__id=instance.id).\
        update(nearest_ohl=None, nearest_ohl_distance=0)


class Motorway(models.Model):
    # Describe an instance of Motorway

    identifier = models.CharField(db_index=True, max_length=255)
    number = models.CharField(max_length=255, blank=True, null=True)
    point = models.PointField(geography=True, spatial_index=True)

    def update_close_locations(self, default_range=1000):
        locations = Location.objects.filter(
            geom__dwithin=(self.point, D(m=default_range))).\
            annotate(distance=Distance('geom', self.point))

        for location in locations:
            if location.nearest_motorway:
                if location.distance.m > location.nearest_motorway_distance:
                    continue

            location.nearest_motorway = self
            location.nearest_motorway_distance = location.distance.m
            location.save()


@receiver(pre_delete, sender=Motorway, weak=False)
def motorway_predelete_handler(sender, instance, **kwargs):
    """
    Whenever we try to delete a Motorway, we search all the Locations
    using it and we remove the reference, so the object can be safely deleted.
    """
    Location.objects.filter(nearest_motorway__id=instance.id).\
        update(nearest_motorway=None, nearest_motorway_distance=0)


class Broadband(models.Model):
    # Describes an instance of Broadband

    postcode = models.CharField(db_index=True, max_length=255)
    point = models.PointField(geography=True, spatial_index=True)
    speed_30_mb_percentage = models.DecimalField(
        max_digits=5, decimal_places=2)
    min_download_speed = models.DecimalField(max_digits=5, decimal_places=2)
    avg_download_speed = models.DecimalField(max_digits=5, decimal_places=2)
    max_download_speed = models.DecimalField(max_digits=5, decimal_places=2)
    min_upload_speed = models.DecimalField(max_digits=5, decimal_places=2)
    avg_upload_speed = models.DecimalField(max_digits=5, decimal_places=2)
    max_upload_speed = models.DecimalField(max_digits=5, decimal_places=2)


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
    nearest_substation = models.ForeignKey(
        Substation, on_delete=models.SET_NULL, null=True)
    nearest_substation_distance = models.FloatField(null=True)  # meters
    nearest_ohl = models.ForeignKey(
        OverheadLine, on_delete=models.SET_NULL, null=True)
    nearest_ohl_distance = models.FloatField(null=True)  # meters
    nearest_motorway = models.ForeignKey(
        Motorway, on_delete=models.SET_NULL, null=True)
    nearest_motorway_distance = models.FloatField(null=True)  # meters

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

    def update_nearest_substation(self, distance=1000):
        sss = Substation.objects.filter(
            geom__dwithin=(self.geom, D(m=distance))).annotate(
            distance=Distance('geom', self.geom)).order_by('distance')

        if len(sss) > 0:
            self.nearest_substation = sss[0]
            self.nearest_substation_distance = sss[0].distance.m

    def update_nearest_overheadline(self, distance=3000):
        oh_lines = OverheadLine.objects.filter(
            geom__dwithin=(self.geom, D(m=distance))).annotate(
            distance=Distance('geom', self.geom)).order_by('distance')

        if len(oh_lines) > 0:
            self.nearest_ohl = oh_lines[0]
            self.nearest_ohl_distance = oh_lines[0].distance.m

    def update_nearest_motorway(self, distance=6000):
        motorways = Motorway.objects.filter(
            point__dwithin=(self.geom, D(m=distance))).annotate(
            distance=Distance('point', self.geom)).order_by('distance')

        if len(motorways) > 0:
            self.nearest_motorway = motorways[0]
            self.nearest_motorway_distance = motorways[0].distance.m

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.update_nearest_busstop()
            self.update_nearest_trainstop()
            self.update_nearest_substation()
            self.update_nearest_overheadline()
            self.update_nearest_motorway()

        super(Location, self).save(*args, **kwargs)
