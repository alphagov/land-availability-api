from .models import (
    BusStop, TrainStop, Address, CodePoint, Broadband, MetroTube, Greenbelt,
    Motorway, Substation, OverheadLine, School, Location)
from rest_framework import serializers
from django.contrib.gis.geos import GEOSGeometry, Point, MultiPolygon
import json


class BusStopSerializer(serializers.ModelSerializer):
    # this extra field is used to specify the srid geo format
    srid = serializers.IntegerField(write_only=True)

    class Meta:
        model = BusStop
        fields = '__all__'

        # We want to handle duplicated entries manually so we remove the
        # unique validator
        extra_kwargs = {
            'amic_code': {
                'validators': [],
            }
        }

    def create(self, validated_data):
        amic_code = validated_data['amic_code']

        try:
            bus_stop = BusStop.objects.get(amic_code=amic_code)
        except BusStop.DoesNotExist:
            bus_stop = BusStop()

        bus_stop.amic_code = validated_data.get('amic_code')
        bus_stop.point = GEOSGeometry(
                validated_data.get('point').geojson,
                srid=validated_data.get('srid'))
        bus_stop.name = validated_data.get('name')
        bus_stop.direction = validated_data.get('direction')
        bus_stop.area = validated_data.get('area')
        bus_stop.road = validated_data.get('road')
        bus_stop.nptg_code = validated_data.get('nptg_code')

        bus_stop.save()
        return bus_stop


class TrainStopSerializer(serializers.ModelSerializer):
    # this extra field is used to specify the srid geo format
    srid = serializers.IntegerField(write_only=True)

    class Meta:
        model = TrainStop
        fields = '__all__'

        # We want to handle duplicated entries manually so we remove the
        # unique validator
        extra_kwargs = {
            'atcode_code': {
                'validators': [],
            }
        }

    def create(self, validated_data):
        atcode_code = validated_data['atcode_code']

        try:
            train_stop = TrainStop.objects.get(atcode_code=atcode_code)
        except TrainStop.DoesNotExist:
            train_stop = TrainStop()

        train_stop.atcode_code = validated_data.get('atcode_code')
        train_stop.naptan_code = validated_data.get('naptan_code')
        train_stop.point = GEOSGeometry(
                validated_data.get('point').geojson,
                srid=validated_data.get('srid'))
        train_stop.name = validated_data.get('name')
        train_stop.main_road = validated_data.get('main_road')
        train_stop.side_road = validated_data.get('side_road')
        train_stop.type = validated_data.get('type')
        train_stop.nptg_code = validated_data.get('nptg_code')
        train_stop.local_reference = validated_data.get('local_reference')

        train_stop.save()
        return train_stop


class AddressSerializer(serializers.ModelSerializer):
    # this extra field is used to specify the srid geo format
    srid = serializers.IntegerField(write_only=True)

    class Meta:
        model = Address
        fields = '__all__'

        # We want to handle duplicated entries manually so we remove the
        # unique validator
        extra_kwargs = {
            'uprn': {
                'validators': [],
            }
        }

    def create(self, validated_data):
        uprn = validated_data['uprn']

        try:
            address = Address.objects.get(uprn=uprn)
        except Address.DoesNotExist:
            address = Address()
            address.uprn = validated_data.get('uprn')

        address.address_line_1 = validated_data.get('address_line_1')
        address.address_line_2 = validated_data.get('address_line_2')
        address.address_line_3 = validated_data.get('address_line_3')
        address.city = validated_data.get('city')
        address.county = validated_data.get('county')
        address.postcode = validated_data.get(
            'postcode').strip().replace(' ', '').upper()
        address.country_code = validated_data.get('country_code')
        address.point = GEOSGeometry(
                validated_data.get('point').geojson,
                srid=validated_data.get('srid'))

        address.save()
        return address


class CodePointSerializer(serializers.ModelSerializer):
    # this extra field is used to specify the srid geo format
    srid = serializers.IntegerField(write_only=True)

    class Meta:
        model = CodePoint
        fields = '__all__'

        # We want to handle duplicated entries manually so we remove the
        # unique validator
        extra_kwargs = {
            'postcode': {
                'validators': [],
            }
        }

    def create(self, validated_data):
        postcode = validated_data['postcode'].strip().replace(' ', '').upper()

        try:
            codepoint = CodePoint.objects.get(postcode=postcode)
        except CodePoint.DoesNotExist:
            codepoint = CodePoint()
            codepoint.postcode = postcode

        codepoint.quality = validated_data.get('quality')
        codepoint.country = validated_data.get('country')
        codepoint.nhs_region = validated_data.get('nhs_region')
        codepoint.nhs_health_authority = validated_data.get(
            'nhs_health_authority')
        codepoint.county = validated_data.get('county')
        codepoint.district = validated_data.get('district')
        codepoint.ward = validated_data.get('ward')
        codepoint.point = GEOSGeometry(
                validated_data.get('point').geojson,
                srid=validated_data.get('srid'))

        codepoint.save()
        return codepoint


class BroadbandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Broadband
        exclude = ('point',)

        # We want to handle duplicated entries manually so we remove the
        # unique validator
        extra_kwargs = {
            'postcode': {
                'validators': [],
            }
        }

    def validate(self, data):
        postcode = data['postcode'].strip().replace(' ', '').upper()

        try:
            codepoint = CodePoint.objects.get(postcode=postcode)
        except CodePoint.DoesNotExist:
            raise serializers.ValidationError(
                "Given postcode does not exist in CodePoint")

        data['postcode'] = postcode
        return data

    def create(self, validated_data):
        postcode = validated_data['postcode']
        codepoint = CodePoint.objects.get(postcode=postcode)

        try:
            broadband = Broadband.objects.get(postcode=postcode)
        except Broadband.DoesNotExist:
            broadband = Broadband()
            broadband.postcode = postcode

        broadband.speed_30_mb_percentage = validated_data.get(
            'speed_30_mb_percentage')
        broadband.min_download_speed = validated_data.get('min_download_speed')
        broadband.avg_download_speed = validated_data.get('avg_download_speed')
        broadband.max_download_speed = validated_data.get('max_download_speed')
        broadband.min_upload_speed = validated_data.get('min_upload_speed')
        broadband.avg_upload_speed = validated_data.get('avg_upload_speed')
        broadband.max_upload_speed = validated_data.get('max_upload_speed')
        broadband.point = codepoint.point

        broadband.save()
        return broadband


class MetroTubeSerializer(serializers.ModelSerializer):
    # this extra field is used to specify the srid geo format
    srid = serializers.IntegerField(write_only=True)

    class Meta:
        model = MetroTube
        fields = '__all__'

        # We want to handle duplicated entries manually so we remove the
        # unique validator
        extra_kwargs = {
            'atco_code': {
                'validators': [],
            },
            'naptan_code': {
                'validators': [],
            }
        }

    def create(self, validated_data):
        atco_code = validated_data['atco_code']

        try:
            metrotube = MetroTube.objects.get(atco_code=atco_code)
        except MetroTube.DoesNotExist:
            metrotube = MetroTube()
            metrotube.atco_code = atco_code

        metrotube.naptan_code = validated_data.get('naptan_code')
        metrotube.name = validated_data.get('name')
        metrotube.locality = validated_data.get('locality')
        metrotube.point = GEOSGeometry(
                validated_data.get('point').geojson,
                srid=validated_data.get('srid'))

        metrotube.save()
        return metrotube


class GreenbeltSerializer(serializers.ModelSerializer):
    # this extra field is used to specify the srid geo format
    srid = serializers.IntegerField(write_only=True)

    class Meta:
        model = Greenbelt
        fields = '__all__'

        # We want to handle duplicated entries manually so we remove the
        # unique validator
        extra_kwargs = {
            'code': {
                'validators': [],
            }
        }

    def create(self, validated_data):
        code = validated_data['code']

        try:
            greenbelt = Greenbelt.objects.get(code=code)
        except Greenbelt.DoesNotExist:
            greenbelt = Greenbelt()
            greenbelt.code = code

        greenbelt.geom = GEOSGeometry(
                validated_data.get('geom').geojson,
                srid=validated_data.get('srid'))
        greenbelt.la_name = validated_data.get('la_name')
        greenbelt.gb_name = validated_data.get('gb_name')
        greenbelt.ons_code = validated_data.get('ons_code')
        greenbelt.year = validated_data.get('year')
        greenbelt.area = validated_data.get('area')
        greenbelt.perimeter = validated_data.get('perimeter')

        greenbelt.save()
        return greenbelt


class MotorwaySerializer(serializers.ModelSerializer):
    # this extra field is used to specify the srid geo format
    srid = serializers.IntegerField(write_only=True)

    class Meta:
        model = Motorway
        fields = '__all__'

        # We want to handle duplicated entries manually so we remove the
        # unique validator
        extra_kwargs = {
            'identifier': {
                'validators': [],
            }
        }

    def create(self, validated_data):
        identifier = validated_data['identifier']

        try:
            motorway = Motorway.objects.get(identifier=identifier)
        except Motorway.DoesNotExist:
            motorway = Motorway()
            motorway.identifier = identifier

        motorway.number = validated_data.get('number')
        motorway.point = GEOSGeometry(
                validated_data.get('point').geojson,
                srid=validated_data.get('srid'))

        motorway.save()
        return motorway


class SubstationSerializer(serializers.ModelSerializer):
    # this extra field is used to specify the srid geo format
    srid = serializers.IntegerField(write_only=True)

    class Meta:
        model = Substation
        fields = '__all__'

        # We want to handle duplicated entries manually so we remove the
        # unique validator
        extra_kwargs = {
            'name': {
                'validators': [],
            }
        }

    def create(self, validated_data):
        name = validated_data['name']

        try:
            substation = Substation.objects.get(name=name)
        except Substation.DoesNotExist:
            substation = Substation()
            substation.name = name

        substation.operating = validated_data.get('operating')
        substation.action_dtt = validated_data.get('action_dtt')
        substation.status = validated_data.get('status')
        substation.description = validated_data.get('description')
        substation.owner_flag = validated_data.get('owner_flag')
        substation.gdo_gid = validated_data.get('gdo_gid')
        substation.geom = GEOSGeometry(
                validated_data.get('geom').geojson,
                srid=validated_data.get('srid'))

        substation.save()
        return substation


class OverheadLineSerializer(serializers.ModelSerializer):
    # this extra field is used to specify the srid geo format
    srid = serializers.IntegerField(write_only=True)

    class Meta:
        model = OverheadLine
        fields = '__all__'

        # We want to handle duplicated entries manually so we remove the
        # unique validator
        extra_kwargs = {
            'gdo_gid': {
                'validators': [],
            }
        }

    def create(self, validated_data):
        gdo_gid = validated_data['gdo_gid']

        try:
            overheadline = OverheadLine.objects.get(gdo_gid=gdo_gid)
        except OverheadLine.DoesNotExist:
            overheadline = OverheadLine()
            overheadline.gdo_gid = gdo_gid

        overheadline.route_asset = validated_data.get('route_asset')
        overheadline.towers = validated_data.get('towers')
        overheadline.action_dtt = validated_data.get('action_dtt')
        overheadline.status = validated_data.get('status')
        overheadline.operating = validated_data.get('operating')
        overheadline.circuit_1 = validated_data.get('circuit_1')
        overheadline.circuit_2 = validated_data.get('circuit_2')
        overheadline.geom = GEOSGeometry(
                validated_data.get('geom').geojson,
                srid=validated_data.get('srid'))

        overheadline.save()
        return overheadline


class SchoolSerializer(serializers.ModelSerializer):
    # this extra field is used to specify the srid geo format
    srid = serializers.IntegerField(write_only=True)

    class Meta:
        model = School
        fields = '__all__'

        # We want to handle duplicated entries manually so we remove the
        # unique validator
        extra_kwargs = {
            'urn': {
                'validators': [],
            }
        }

    def create(self, validated_data):
        urn = validated_data['urn']

        try:
            school = School.objects.get(urn=urn)
        except School.DoesNotExist:
            school = School()
            school.urn = urn

        school.la_name = validated_data.get('la_name')
        school.school_name = validated_data.get('school_name')
        school.school_type = validated_data.get('school_type')
        school.school_capacity = validated_data.get('school_capacity')
        school.school_pupils = validated_data.get('school_capacity')
        school.postcode = validated_data.get('postcode')
        school.point = GEOSGeometry(
            validated_data.get('point').geojson,
            srid=validated_data.get('srid'))

        school.save()
        return school


class LocationSerializer(serializers.ModelSerializer):
    # this extra field is used to specify the srid geo format
    srid = serializers.IntegerField(write_only=True)
    site_size = serializers.SerializerMethodField()

    class Meta:
        model = Location
        fields = (
            'id', 'uprn', 'ba_ref', 'name', 'point', 'geom',
            'authority', 'owner', 'unique_asset_id', 'full_address',
            'estimated_floor_space', 'nearest_busstop_id',
            'nearest_busstop_distance', 'nearest_trainstop_id',
            'nearest_trainstop_distance', 'nearest_substation_id',
            'nearest_substation_distance', 'nearest_ohl_id',
            'nearest_ohl_distance', 'nearest_motorway_id',
            'nearest_motorway_distance', 'nearest_broadband_id',
            'nearest_broadband_distance', 'nearest_broadband_fast',
            'greenbelt_overlap',
            'nearest_primary_school_id', 'nearest_primary_school_distance',
            'nearest_secondary_school_id',
            'nearest_secondary_school_distance', 'nearest_metrotube_id',
            'nearest_metrotube_distance', 'site_size', 'srid'
            )

        # We want to handle duplicated entries manually so we remove the
        # unique validator
        extra_kwargs = {
            'uprn': {
                'validators': [],
            },
            'point': {
                'validators': [],
            },
        }

    def get_site_size(self, obj):
        return obj.get_geom_area()

    def create(self, validated_data):
        uprn = validated_data['uprn']

        try:
            location = Location.objects.get(uprn=uprn)
        except Location.DoesNotExist:
            location = Location()
            location.uprn = uprn

        location.ba_ref = validated_data.get('ba_ref')
        location.geom = GEOSGeometry(
            validated_data.get('geom').geojson,
            srid=validated_data.get('srid'))
        centroid = location.geom.centroid
        # sanity check - centroid function gives a point in Africa for uprn
        # 200004165968!
        if centroid.distance(location.geom) < 10:
            location.point = centroid
        else:
            # just set it to the first point in the polygon. if we leave it
            # blank then the map is blank.
            assert isinstance(location.geom, MultiPolygon)
            location.point = Point(location.geom.coords[0][0][0])
        location.name = validated_data.get('name')
        location.authority = validated_data.get('authority')
        location.owner = validated_data.get('owner')
        location.unique_asset_id = validated_data.get('unique_asset_id')
        location.full_address = validated_data.get('full_address')
        location.estimated_floor_space = validated_data.get('estimated_floor_space')

        location.save()
        return location
