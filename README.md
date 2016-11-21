# land-avilability-api
API backend for Land Availability tool

# PostgreSQL Setup

Make sure you have **PostgreSQL** (tested with 9.6) installed along with PostGIS
extension. You can find more information for the different operating systems
here: https://docs.djangoproject.com/en/1.10/ref/contrib/gis/install/postgis/

It's strongly suggested to use Postgres.app on OSX and to install all the other
tools and dependencies using **brew**.

## Create DB

```
createdb landavailability
psql landavailability
> CREATE EXTENSION postgis;
```

# Project Configuration

Make sure you have these environment variables set:

```
LANDAVAILABILITY_DB_NAME=landavailability
LANDAVAILABILITY_DB_USER=youruser
LANDAVAILABILITY_DB_PASSWORD=yourpassword
LANDAVAILABILITY_DB_HOST=localhost
LANDAVAILABILITY_DB_PORT=5432
```

If you are using a Python virtual environment, you can save these values in
$venv_folder/bin/postactivate script:

```
export LANDAVAILABILITY_DB_NAME=landavailability
export LANDAVAILABILITY_DB_USER=youruser
export LANDAVAILABILITY_DB_PASSWORD=yourpassword
export LANDAVAILABILITY_DB_HOST=localhost
export LANDAVAILABILITY_DB_PORT=5432
```
