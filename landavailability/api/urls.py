from django.conf.urls import url
from . import views

urlpatterns = [
    url(
        r'^busstops/$',
        views.BusStopCreateView.as_view(), name='busstops-create'),
    url(
        r'^trainstops/$',
        views.TrainStopCreateView.as_view(), name='trainstops-create'),
    url(
        r'^addresses/$',
        views.AddressCreateView.as_view(), name='addresses-create'),
    url(
        r'^codepoints/$',
        views.CodePointCreateView.as_view(), name='codepoints-create'),
    url(
        r'^broadbands/$',
        views.BroadbandCreateView.as_view(), name='broadbands-create'),
    url(
        r'^metrotubes/$',
        views.MetroTubeCreateView.as_view(), name='metrotubes-create'),
    url(
        r'^greenbelts/$',
        views.GreenbeltCreateView.as_view(), name='greenbelts-create'),
    url(
        r'^motorways/$',
        views.MotorwayCreateView.as_view(), name='motorways-create'),
    url(
        r'^substations/$',
        views.SubstationCreateView.as_view(), name='substations-create'),
    url(
        r'^overheadlines/$',
        views.OverheadLineCreateView.as_view(), name='overheadlines-create'),
    url(
        r'^schools/$',
        views.SchoolCreateView.as_view(), name='schools-create'),
    url(
        r'^locations/$',
        views.LocationView.as_view(), name='locations'),
]
