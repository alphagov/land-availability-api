from django.conf.urls import url
from . import views

urlpatterns = [
    url(
        r'^busstop/$',
        views.BusStopCreateView.as_view(), name='busstop-create'),
]
