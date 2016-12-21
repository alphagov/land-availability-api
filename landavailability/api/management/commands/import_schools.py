from django.contrib.gis.geos import Point
from api.models import School
from .importers import CSVImportCommand


class Command(CSVImportCommand):
    help = 'Import schools from a CSV file'

    def __init__(self):
        super().__init__(skip_header=True, encoding='ISO-8859-1')

    def process_row(self, row):
        print('{0} - {1}'.format(row[0], row[4]))

        # Only import schools with easting and northing information
        if row[68] and row[69]:
            try:
                school = School.objects.get(urn=row[0])
            except School.DoesNotExist:
                school = School()
                school.urn = row[0]

            school.la_name = row[2]
            school.school_name = row[4]
            school.school_type = row[11]

            if row[20]:
                school.school_capacity = int(row[20])

            if row[23]:
                school.school_pupils = int(row[23])

            school.postcode = row[44].replace(' ', '')
            school.point = Point(float(row[68]), float(row[69]), srid=27700)

            try:
                school.save()
                school.update_close_locations()
            except Exception as e:
                print('Could not add: {0} because {1}'.format(row, e))
