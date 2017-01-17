from django.conf.urls import url
from . import views

urlpatterns = [
    url(
        r'^busstop/$',
        views.BusStopCreateView.as_view(), name='busstop-create'),
    url(
        r'^trainstop/$',
        views.TrainStopCreateView.as_view(), name='trainstop-create'),
    url(
        r'^address/$',
        views.AddressCreateView.as_view(), name='address-create'),
    url(
        r'^codepoint/$',
        views.CodePointCreateView.as_view(), name='codepoint-create'),
    url(
        r'^broadband/$',
        views.BroadbandCreateView.as_view(), name='broadband-create'),
    url(
        r'^metrotube/$',
        views.MetroTubeCreateView.as_view(), name='metrotube-create'),
]
