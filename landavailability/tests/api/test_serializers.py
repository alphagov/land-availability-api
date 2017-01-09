from unittest import TestCase
import pytest
import json
from api.models import BusStop, TrainStop
from api.serializers import BusStopSerializer, TrainStopSerializer


class TestBusStopSerializer(TestCase):
    @pytest.mark.django_db
    def test_busstop_serializer_create_object(self):
        json_payload = """
            {
                "amic_code": "1800AMIC001",
                "point": {
                    "type": "Point",
                    "coordinates": [-2.347743000012108,53.38737090322739]
                },
                "name": "Altrincham Interchange",
                "direction": "Nr Train Station",
                "area": "NA",
                "road": "STAMFORD NEW RD",
                "nptg_code": "E0028261",
                "srid": 4326
            }
        """

        data = json.loads(json_payload)
        serializer = BusStopSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        serializer.save()
        self.assertEqual(BusStop.objects.count(), 1)


class TestTrainStopSerializer(TestCase):
    @pytest.mark.django_db
    def test_trainstop_serializer_create_object(self):
        json_payload = """
            {
                "atcode_code": "9100ALTRNHM",
                "naptan_code": "",
                "point": {
                    "type": "Point",
                    "coordinates": [377008, 387924]
                },
                "name": "DATALAND INTERCHANGE",
                "main_road": "DATALAND NEW RD",
                "side_road": "DATA LANE",
                "type": "R",
                "nptg_code": "E0028261",
                "local_reference": "AA123ZZ",
                "srid": 27700
            }
        """

        data = json.loads(json_payload)
        serializer = TrainStopSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        serializer.save()
        self.assertEqual(TrainStop.objects.count(), 1)
