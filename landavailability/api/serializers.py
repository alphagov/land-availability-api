from .models import BusStop
from rest_framework import serializers
from django.contrib.gis.geos import GEOSGeometry
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
