from django.core.management.base import BaseCommand, CommandError
from api.models import BusStop


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        bss = BusStop.objects.all()
        total_busses = len(bss)

        for i, bs in enumerate(bss):
            print('Processing bus: {0} of {1}'.format(i, total_busses))
            bs.update_close_locations()
