from .models import BusStop
from rest_framework import serializers


class BusStopSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusStop
        fields = '__all__'
