from django.contrib.gis.db import models
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from django.db.models.signals import pre_delete
from django.dispatch import receiver


class Address(models.Model):
    # Describes an instance of an address

    uprn = models.CharField(unique=True, max_length=100)
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

    postcode = models.CharField(unique=True, max_length=20)
    quality = models.IntegerField(null=True)
    point = models.PointField(geography=True, spatial_index=True)
    country = models.CharField(null=True, blank=True, max_length=24)
    nhs_region = models.CharField(null=True, blank=True, max_length=24)
    nhs_health_authority = models.CharField(
        null=True, blank=True, max_length=24)
    county = models.CharField(null=True, blank=True, max_length=24)
    district = models.CharField(null=True, blank=True, max_length=24)
    ward = models.CharField(null=True, blank=True, max_length=24)


class BusStop(models.Model):
    # Describes an instance of a bus stop

    amic_code = models.CharField(unique=True, max_length=20)
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

    atcode_code = models.CharField(unique=True, max_length=24)
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

    name = models.CharField(unique=True, max_length=255)
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

    gdo_gid = models.CharField(unique=True, max_length=255)
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

    identifier = models.CharField(unique=True, max_length=255)
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

    postcode = models.CharField(unique=True, max_length=255)
    point = models.PointField(geography=True, spatial_index=True)
    speed_30_mb_percentage = models.DecimalField(
        max_digits=5, decimal_places=2, null=True)
    min_download_speed = models.DecimalField(
        max_digits=5, decimal_places=2, null=True)
    avg_download_speed = models.DecimalField(
        max_digits=5, decimal_places=2, null=True)
    max_download_speed = models.DecimalField(
        max_digits=5, decimal_places=2, null=True)
    min_upload_speed = models.DecimalField(
        max_digits=5, decimal_places=2, null=True)
    avg_upload_speed = models.DecimalField(
        max_digits=5, decimal_places=2, null=True)
    max_upload_speed = models.DecimalField(
        max_digits=5, decimal_places=2, null=True)

    def update_close_locations(self, default_range=1000):
        locations = Location.objects.filter(
            geom__dwithin=(self.point, D(m=default_range))).\
            annotate(distance=Distance('geom', self.point))

        for location in locations:
            if location.nearest_broadband:
                if location.distance.m > location.nearest_broadband_distance:
                    continue

            location.nearest_broadband = self
            location.nearest_broadband_distance = location.distance.m

            if self.speed_30_mb_percentage > 0:
                location.nearest_broadband_fast = True

            location.save()


@receiver(pre_delete, sender=Broadband, weak=False)
def broadband_predelete_handler(sender, instance, **kwargs):
    """
    Whenever we try to delete a Broadband, we search all the Locations
    using it and we remove the reference, so the object can be safely deleted.
    """
    Location.objects.filter(nearest_broadband__id=instance.id).\
        update(
            nearest_broadband=None,
            nearest_broadband_distance=0,
            nearest_broadband_fast=False)


class Greenbelt(models.Model):
    # Describes an instance of a greenbelt

    code = models.CharField(unique=True, max_length=255)
    la_name = models.CharField(max_length=255, blank=True, null=True)
    gb_name = models.CharField(max_length=255, blank=True, null=True)
    ons_code = models.CharField(max_length=255, blank=True, null=True)
    year = models.CharField(max_length=255, blank=True, null=True)
    area = models.DecimalField(max_digits=9, decimal_places=2, null=True)
    perimeter = models.DecimalField(max_digits=9, decimal_places=2, null=True)
    geom = models.MultiPolygonField(geography=True, spatial_index=True)

    def update_close_locations(self, default_range=1000):
        locations = Location.objects.filter(
            geom__dwithin=(self.geom, D(m=default_range))).\
            annotate(distance=Distance('geom', self.geom))

        for location in locations:
            if location.nearest_greenbelt:
                if location.distance.m > location.nearest_greenbelt_distance:
                    continue

            location.nearest_greenbelt = self
            location.nearest_greenbelt_distance = location.distance.m
            location.save()


@receiver(pre_delete, sender=Greenbelt, weak=False)
def greenbelt_predelete_handler(sender, instance, **kwargs):
    """
    Whenever we try to delete a Greenbelt, we search all the Locations
    using it and we remove the reference, so the object can be safely deleted.
    """
    Location.objects.filter(nearest_greenbelt__id=instance.id).\
        update(
            nearest_greenbelt=None,
            nearest_greenbelt_distance=0)


class School(models.Model):
    # Describes an instance of a School

    urn = models.CharField(db_index=True, max_length=255)
    la_name = models.CharField(max_length=255, blank=True, null=True)
    school_name = models.CharField(max_length=255, blank=True, null=True)
    school_type = models.CharField(max_length=255, blank=True, null=True)
    school_capacity = models.IntegerField(null=True)
    school_pupils = models.IntegerField(null=True)
    postcode = models.CharField(max_length=255, blank=True, null=True)
    point = models.PointField(geography=True, spatial_index=True)

    def update_close_locations(self, default_range=1000):
        locations = Location.objects.filter(
            geom__dwithin=(self.point, D(m=default_range))).\
            annotate(distance=Distance('geom', self.point))

        for location in locations:
            if location.nearest_school:
                if location.distance.m > location.nearest_school_distance:
                    continue

            location.nearest_school = self
            location.nearest_school_distance = location.distance.m
            location.save()


@receiver(pre_delete, sender=School, weak=False)
def school_predelete_handler(sender, instance, **kwargs):
    """
    Whenever we try to delete a School, we search all the Locations
    using it and we remove the reference, so the object can be safely deleted.
    """
    Location.objects.filter(nearest_school__id=instance.id).\
        update(
            nearest_school=None,
            nearest_school_distance=0)


class MetroTube(models.Model):
    # Describes an instance of a Metro or a Tube stop

    atco_code = models.CharField(unique=True, max_length=255)
    naptan_code = models.CharField(db_index=True, max_length=255)
    name = models.CharField(max_length=255, blank=True, null=True)
    locality = models.CharField(max_length=255, blank=True, null=True)
    point = models.PointField(geography=True, spatial_index=True)

    def update_close_locations(self, default_range=1000):
        locations = Location.objects.filter(
            geom__dwithin=(self.point, D(m=default_range))).\
            annotate(distance=Distance('geom', self.point))

        for location in locations:
            if location.nearest_metrotube:
                if location.distance.m > location.nearest_metrotube_distance:
                    continue

            location.nearest_metrotube = self
            location.nearest_metrotube_distance = location.distance.m
            location.save()


@receiver(pre_delete, sender=MetroTube, weak=False)
def metrotube_predelete_handler(sender, instance, **kwargs):
    """
    Whenever we try to delete a MetroTube, we search all the Locations
    using it and we remove the reference, so the object can be safely deleted.
    """
    Location.objects.filter(nearest_metrotube__id=instance.id).\
        update(
            nearest_metrotube=None,
            nearest_metrotube_distance=0)


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
    nearest_broadband = models.ForeignKey(
        Broadband, on_delete=models.SET_NULL, null=True)
    nearest_broadband_distance = models.FloatField(null=True)  # meters
    nearest_broadband_fast = models.NullBooleanField()
    nearest_greenbelt = models.ForeignKey(
        Greenbelt, on_delete=models.SET_NULL, null=True)
    nearest_greenbelt_distance = models.FloatField(null=True)  # meters
    nearest_school = models.ForeignKey(
        School, on_delete=models.SET_NULL, null=True)
    nearest_school_distance = models.FloatField(null=True)  # meters
    nearest_metrotube = models.ForeignKey(
        MetroTube, on_delete=models.SET_NULL, null=True)
    nearest_metrotube_distance = models.FloatField(null=True)  # meters

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

    def update_nearest_broadband(self, distance=500):
        broadbands = Broadband.objects.filter(
            point__dwithin=(self.geom, D(m=distance))).annotate(
            distance=Distance('point', self.geom)).order_by('distance')

        if len(broadbands) > 0:
            self.nearest_broadband = broadbands[0]
            self.nearest_broadband_distance = broadbands[0].distance.m
            if broadbands[0].speed_30_mb_percentage > 0:
                self.nearest_broadband_fast = True

    def update_nearest_greenbelt(self, distance=500):
        greenbelts = Greenbelt.objects.filter(
            geom__dwithin=(self.geom, D(m=distance))).annotate(
            distance=Distance('geom', self.geom)).order_by('distance')

        if len(greenbelts) > 0:
            self.nearest_greenbelt = greenbelts[0]
            self.nearest_greenbelt_distance = greenbelts[0].distance.m

    def update_nearest_school(self, distance=1000):
        schools = School.objects.filter(
            point__dwithin=(self.geom, D(m=distance))).annotate(
            distance=Distance('point', self.geom)).order_by('distance')

        if len(schools) > 0:
            self.nearest_school = schools[0]
            self.nearest_school_distance = schools[0].distance.m

    def update_nearest_metrotube(self, distance=1000):
        metrotubes = MetroTube.objects.filter(
            point__dwithin=(self.geom, D(m=distance))).annotate(
            distance=Distance('point', self.geom)).order_by('distance')

        if len(metrotubes) > 0:
            self.nearest_metrotube = metrotubes[0]
            self.nearest_metrotube_distance = metrotubes[0].distance.m

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.update_nearest_busstop()
            self.update_nearest_trainstop()
            self.update_nearest_substation()
            self.update_nearest_overheadline()
            self.update_nearest_motorway()
            self.update_nearest_broadband()
            self.update_nearest_greenbelt()
            self.update_nearest_school()
            self.update_nearest_metrotube()

        super(Location, self).save(*args, **kwargs)
