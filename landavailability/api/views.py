from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from .models import BusStop
from .serializers import BusStopSerializer


class BusStopCreateView(generics.CreateAPIView):
    queryset = BusStop.objects.all()
    serializer_class = BusStopSerializer
    permission_classes = (IsAdminUser, )

    def perform_create(self, serializer):
        if serializer.is_valid():
            amic_code = serializer.validated_data['amic_code']

            try:
                bus_stop = BusStop.objects.get(amic_code=amic_code)
                bus_stop.point = serializer.validated_data['point']
                bus_stop.name = serializer.validated_data['name']
                bus_stop.direction = serializer.validated_data['direction']
                bus_stop.area = serializer.validated_data['area']
                bus_stop.road = serializer.validated_data['road']
                bus_stop.nptg_code = serializer.validated_data['nptg_code']
                bus_stop.save()
            except BusStop.DoesNotExist:
                instance = serializer.save()

            instance.update_close_locations()
