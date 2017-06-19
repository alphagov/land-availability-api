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
from django.db.models.query import QuerySet
import json
from .permissions import IsAdminOrReadOnlyUser

log = __import__('logging').getLogger(__name__)


MIN_PAGE_SIZE = 1
MAX_PAGE_SIZE = 100

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
        build = request.query_params.get('build')
        num_pupils = request.query_params.get('num_pupils', 0)
        num_pupils_post16 = request.query_params.get('num_pupils_post16', 0)
        page = request.query_params.get('page', 1)
        page_size = request.query_params.get('page_size', 20)

        try:
            num_pupils = int(num_pupils)
        except ValueError:
            log.info('num_pupils parameter must be an integer not %r',
                     num_pupils)
            return Response('num_pupils parameter must be an integer',
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            num_pupils_post16 = int(num_pupils_post16)
        except ValueError:
            log.info('num_pupils_post16 parameter must be an integer not %r',
                     num_pupils_post16)
            return Response('num_pupils_post16 parameter must be an integer',
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            page_size = int(page_size)
        except ValueError:
            log.info('page_size parameter must be an integer not %r',
                     page_size)
            return Response('page_size parameter must be an integer',
                            status=status.HTTP_400_BAD_REQUEST)
        if page_size > MAX_PAGE_SIZE:
            log.info('page_size parameter %r is above max %s',
                     page_size, MAX_PAGE_SIZE)
            return Response('page_size maximum is {}'.format(MAX_PAGE_SIZE),
                            status=status.HTTP_400_BAD_REQUEST)
        if page_size < MIN_PAGE_SIZE:
            log.info('page_size parameter %r is below min %s',
                     page_size, MIN_PAGE_SIZE)
            return Response('page_size minimum is {}'.format(MIN_PAGE_SIZE),
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            page = int(page)
        except ValueError:
            log.info('page parameter must be an integer not %r',
                     page)
            return Response('page parameter must be an integer',
                            status=status.HTTP_400_BAD_REQUEST)
        if page < 1:
            log.info('page parameter must be 1 or above not %r',
                     page)
            return Response('page must be 1 or above',
                            status=status.HTTP_400_BAD_REQUEST)

        # work out which locations are requested
        if polygon:
            # Build a Polygon instance using the coordinates passed
            # as parameters in the 'polygon' field of the query string
            json_geometry = {
                "type": "Polygon",
                "coordinates": json.loads(polygon)
            }

            geometry = GEOSGeometry(json.dumps(json_geometry), srid=4326)

            # Get all the locations that intersect the given polygon
            locations = Location.objects.filter(geom__intersects=geometry).\
                order_by('id')
        elif postcode and range_distance:
            # Normalise postcode first
            postcode = postcode.replace(' ', '').upper()

            try:
                codepoint = CodePoint.objects.get(postcode=postcode)
            except CodePoint.DoesNotExist:
                log.info('postcode %s not found in CodePoint', postcode)
                return Response(
                    'The given postcode is not available in CodePoint',
                    status=status.HTTP_400_BAD_REQUEST)

            locations = Location.objects.filter(
                geom__dwithin=(codepoint.point, D(m=range_distance))).\
                order_by('id').\
                annotate(distance=Distance('geom', codepoint.point))
        else:
            log.info('Params missing postcode and range_distance OR '
                     'polygon')
            return Response(
                'The parameters are missing: postcode and range_distance OR '
                'polygon',
                status=status.HTTP_400_BAD_REQUEST)

        # serialize them
        from .ranking import (school_site_size_range,
                              score_results_dataframe,
                              SchoolRankingConfig,
                              )
        return_data = {}

        # score & order them
        if build and locations:
            if build not in ('secondary_school', 'primary_school'):
                log.info('build should be "secondary_school" or '
                         '"primary_school" not %r', build)
                return Response('Bad parameter "build" - should be '
                                '"secondary_school" or "primary_school"',
                                status=status.HTTP_400_BAD_REQUEST)
            lower_site_req, upper_site_req = school_site_size_range(**kwargs)
            return_data.update({
                'lower_site_req': lower_site_req,
                'upper_site_req': upper_site_req,
                })
            ranking_config = SchoolRankingConfig(
                lower_site_req=lower_site_req, upper_site_req=upper_site_req,
                school_type=build)
            locations = ranking_config.locations_to_dataframe(locations)
            ranking_config.extract_features(locations)
            scored_locations = score_results_dataframe(locations,
                                                       ranking_config)

        # paging
        offset = page_size * (page - 1)
        if offset > len(locations):
            log.info('Page %s is out of range', offset)
            return Response('"page" is out of range',
                            status=status.HTTP_404_NOT_FOUND)
        locations_to_show = locations[offset:offset + page_size]

        # convert to Location objects
        # also consider just returning JSON with the score and scoring details
        if isinstance(locations, QuerySet):
            location_ids = [l.id for l in locations_to_show]
        else:
            # locations is a dataframe, because they have been ranked
            location_ids = locations_to_show.index
        location_objs = Location.objects.filter(id__in=location_ids).\
            order_by('id')
        # sort by score
        if build:
            location_objs_and_ranking_info = [
                merge_dicts(
                    LocationSerializer(location_obj).data,
                    scored_locations.iloc[[i]].to_dict(orient='records')[0])
                for i, location_obj in enumerate(location_objs)
                ]
            location_objs_and_ranking_info.sort(
                key=lambda x: -x['score']
                )
            log.debug('Scores: %s',
                      [(l['name'], l['score'])
                       for l in location_objs_and_ranking_info]
                      )
            return_data['locations'] = location_objs_and_ranking_info
        else:
            serializer = LocationSerializer(location_objs, many=True)
            return_data['locations'] = serializer.data

        return Response(return_data, status=status.HTTP_200_OK)

def merge_dicts(*dict_args):
    """
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    """
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result


class LocationDetailsView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    lookup_field = 'uprn'
    lookup_url_kwarg = 'uprn'
