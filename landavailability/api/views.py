from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from .models import BusStop
from .serializers import BusStopSerializer


class BusStopCreateView(generics.CreateAPIView):
    queryset = BusStop.objects.all()
    serializer_class = BusStopSerializer
    permission_classes = (IsAdminUser, )

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.update_close_locations()
