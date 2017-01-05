from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from .models import BusStop
from .serializers import BusStopSerializer


class BusStopCreateView(APIView):
    permission_classes = (IsAdminUser, )

    def post(self, request, format=None):
        import ipdb; ipdb.set_trace()
        serializer = BusStopSerializer(data=request.data)

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
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
