from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from .models import BusStop
from .serializers import BusStopSerializer
from django.contrib.gis.geos import GEOSGeometry


class BusStopCreateView(APIView):
    permission_classes = (IsAdminUser, )

    def post(self, request, format=None):
        serializer = BusStopSerializer(data=request.data)

        if serializer.is_valid():
            bus_stop = serializer.save()
            bus_stop.update_close_locations()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
