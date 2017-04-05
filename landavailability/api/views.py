from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .models import (
    BusStop, TrainStop, Address, CodePoint, Broadband, MetroTube, Greenbelt,
    Motorway, Substation, OverheadLine, School, Location)
from .serializers import (
    BusStopSerializer, TrainStopSerializer, AddressSerializer,
    CodePointSerializer, BroadbandSerializer, MetroTubeSerializer,
    GreenbeltSerializer, MotorwaySerializer, SubstationSerializer,
    OverheadLineSerializer, SchoolSerializer, LocationSerializer)
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
import json
from .permissions import IsAdminOrReadOnlyUser


class BusStopCreateView(APIView):
    permission_classes = (IsAdminUser, )

    def post(self, request, format=None):
        serializer = BusStopSerializer(data=request.data)

        if serializer.is_valid():
            bus_stop = serializer.save()
            bus_stop.update_close_locations()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TrainStopCreateView(APIView):
    permission_classes = (IsAdminUser, )

    def post(self, request, format=None):
        serializer = TrainStopSerializer(data=request.data)

        if serializer.is_valid():
            train_stop = serializer.save()
            train_stop.update_close_locations()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddressCreateView(APIView):
    permission_classes = (IsAdminUser, )

    def post(self, request, format=None):
        serializer = AddressSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CodePointCreateView(APIView):
    permission_classes = (IsAdminUser, )

    def post(self, request, format=None):
        serializer = CodePointSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BroadbandCreateView(APIView):
    permission_classes = (IsAdminUser, )

    def post(self, request, format=None):
        serializer = BroadbandSerializer(data=request.data)

        if serializer.is_valid():
            broadband = serializer.save()
            broadband.update_close_locations()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MetroTubeCreateView(APIView):
    permission_classes = (IsAdminUser, )

    def post(self, request, format=None):
        serializer = MetroTubeSerializer(data=request.data)

        if serializer.is_valid():
            metrotube = serializer.save()
            metrotube.update_close_locations()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GreenbeltCreateView(APIView):
    permission_classes = (IsAdminUser, )

    def post(self, request, format=None):
        serializer = GreenbeltSerializer(data=request.data)

        if serializer.is_valid():
            greenbelt = serializer.save()
            greenbelt.update_close_locations()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MotorwayCreateView(APIView):
    permission_classes = (IsAdminUser, )

    def post(self, request, format=None):
        serializer = MotorwaySerializer(data=request.data)

        if serializer.is_valid():
            motorway = serializer.save()
            motorway.update_close_locations()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubstationCreateView(APIView):
    permission_classes = (IsAdminUser, )

    def post(self, request, format=None):
        serializer = SubstationSerializer(data=request.data)

        if serializer.is_valid():
            substation = serializer.save()
            substation.update_close_locations()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OverheadLineCreateView(APIView):
    permission_classes = (IsAdminUser, )

    def post(self, request, format=None):
        serializer = OverheadLineSerializer(data=request.data)

        if serializer.is_valid():
            overheadline = serializer.save()
            overheadline.update_close_locations()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SchoolCreateView(APIView):
    permission_classes = (IsAdminUser, )

    def post(self, request, format=None):
        serializer = SchoolSerializer(data=request.data)

        if serializer.is_valid():
            school = serializer.save()
            school.update_close_locations()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LocationView(APIView):
    permission_classes = (IsAdminOrReadOnlyUser, )

    def post(self, request, format=None):
        serializer = LocationSerializer(data=request.data)

        if serializer.is_valid():
            school = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        postcode = request.query_params.get('postcode')
        range_distance = request.query_params.get('range_distance')
        polygon = request.query_params.get('polygon')

        if polygon:
            # Build a Polygon instance using the coordinates passed
            # as parameters in the 'polygon' field of the query string
            json_geometry = {
                "type": "Polygon",
                "coordinates": json.loads(polygon)
            }

            geometry = GEOSGeometry(json.dumps(json_geometry), srid=4326)

            # Get all the locations that intersect the given polygon
            locations = Location.objects.filter(geom__intersects=geometry)
            serializer = LocationSerializer(locations, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif postcode and range_distance:
            # Normalise postcode first
            postcode = postcode.replace(' ', '').upper()

            try:
                codepoint = CodePoint.objects.get(postcode=postcode)
            except CodePoint.DoesNotExist as ex:
                return Response(
                    'The given postcode is not available in CodePoints',
                    status=status.HTTP_400_BAD_REQUEST)

            locations = Location.objects.filter(
                geom__dwithin=(codepoint.point, D(m=range_distance))).\
                annotate(distance=Distance('geom', codepoint.point))
            serializer = LocationSerializer(locations, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                'The postcode parameter is missing',
                status=status.HTTP_400_BAD_REQUEST)


class LocationDetailsView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    lookup_field = 'uprn'
    lookup_url_kwarg = 'uprn'
