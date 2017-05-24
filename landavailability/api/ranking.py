import pandas as pd
from pandas.io.json import json_normalize
import numpy as np

log = __import__('logging').getLogger(__file__)


def school_site_size_range_from_terms(terms):
    return school_site_size_range(
        num_pupils=terms.get('pupils', 0),
        num_pupils_post16=terms.get('post16', 0),
        school_type=terms.get('build'),
        )

def school_site_size_range(**kwargs):
    # size_req on ola
    size = school_site_size(**kwargs)
    # upper_site_req, lower_site_req on ola
    size_range = (size * 0.95, size * 1.5)
    return size_range

def school_site_size(num_pupils=0,
                     num_pupils_post16=0,
                     school_type='primary_school'):
    '''Return the expected floor space (m^2) for the given parameters.
    NB pupils post-16 should be included both figures 'num_pupils' and
    'num_pupils_post16'.
    '''
    if school_type == 'secondary_school':
        # Deal with sixth form additional space
        if num_pupils_post16 > 0:
            under16 = num_pupils - num_pupils_post16
            return (1050.0 + (6.3 * under16)) + \
                   (350 + (7 * float(num_pupils_post16)))
        else:
            return 1050 + (6.3 * float(num_pupils))
    elif school_type == 'primary_school':
        return 350.0 + (4.1 * float(num_pupils))
    else:  # default to primary_school
        return 350.0 + (4.1 * float(num_pupils))
    return 0


SCORING_COLUMNS = [
    'area_suitable',
    'geoattributes.BROADBAND',
    'geoattributes.COVERAGE BY GREENBELT',
    'geoattributes.DISTANCE TO BUS STOP',
    'geoattributes.DISTANCE TO METRO STATION',
    'geoattributes.DISTANCE TO MOTORWAY JUNCTION',
    'geoattributes.DISTANCE TO OVERHEAD LINE',
    'geoattributes.DISTANCE TO PRIMARY SCHOOL',
    'geoattributes.DISTANCE TO RAIL STATION',
    'geoattributes.DISTANCE TO SECONDARY SCHOOL',
    'geoattributes.DISTANCE TO SUBSTATION'
    ]

def locations_to_dataframe(locations):
    df = pd.DataFrame([
        {
            'geoattributes.AREA': l.estimated_floor_space,
            'geoattributes.BROADBAND': 1.0 if l.nearest_broadband_fast else 0.0,
            'geoattributes.COVERAGE BY GREENBELT': np.NaN,  # TODO
            'geoattributes.DISTANCE TO BUS STOP': l.nearest_busstop_distance,
            'geoattributes.DISTANCE TO METRO STATION': l.nearest_metrotube_distance,
            'geoattributes.DISTANCE TO MOTORWAY JUNCTION': l.nearest_motorway_distance,
            'geoattributes.DISTANCE TO OVERHEAD LINE': l.nearest_ohl_distance,
            'geoattributes.DISTANCE TO PRIMARY SCHOOL': l.nearest_primary_school_distance,
            'geoattributes.DISTANCE TO RAIL STATION': l.nearest_trainstop_distance,
            'geoattributes.DISTANCE TO SECONDARY SCHOOL': l.nearest_secondary_school_distance,
            'geoattributes.DISTANCE TO SUBSTATION': l.nearest_substation_distance,
            }
        for l in locations
        ],
        index=[l.id for l in locations])
    df = df.apply(lambda x: pd.to_numeric(x, errors='ignore'))
    return df


def score_result_dicts(result_dicts, lower_site_req, upper_site_req,
                       school_type):
    # convert dict results to a DataFrame
    df = json_normalize(result_dicts)
    # '67' -> 67
    df['geoattributes.BROADBAND'] = \
        pd.to_numeric(df['geoattributes.BROADBAND'], errors='ignore')

    # do the scoring
    df_scored = score_results_dataframe(
        df, lower_site_req, upper_site_req, school_type)

    # bundle up the score and search result
    df_final = json_normalize(result_dicts)
    df_final = pd.concat(
        [df_final, df_scored[['score']], df[['area_suitable']]],
        axis=1)
    return df_final

def score_results_dataframe(results_dataframe, lower_site_req, upper_site_req,
                            school_type):
    '''Given search results (location) as rows of a dataframe (with columns
    roughly SCORING_COLUMNS), return another dataframe with those rows and
    a column 'score'. A higher score means a higher suitability for building
    the specified school.

    '''
    df = results_dataframe

    # work out if the site size is suitable
    calculate_is_area_suitable(df, lower_site_req, upper_site_req)

    # filter to only the columns that we'll score against
    df2 = pd.concat([df[col] for col in SCORING_COLUMNS], axis=1)

    # TODO
    # Check that distances are correctly either euclidean or network.
    # Network:
    #   'geoattributes.DISTANCE TO BUS STOP_zscore',
    #   'geoattributes.DISTANCE TO METRO STATION_zscore',
    #   'geoattributes.DISTANCE TO PRIMARY SCHOOL_zscore',
    #   'geoattributes.DISTANCE TO RAIL STATION_zscore',
    #   'geoattributes.DISTANCE TO SECONDARY SCHOOL_zscore'
    # Euclidean:
    #   'geoattributes.DISTANCE TO MOTORWAY JUNCTION',
    #   'geoattributes.DISTANCE TO OVERHEAD LINE',
    #   'geoattributes.DISTANCE TO SUBSTATION'

    # z-score scaling
    # (not really necessary because we scale it again, but useful for
    #  analysis)
    if False:
        z_score_scaling(df2)

    # Rescale minimum = 0 and maximum = 1 for each column
    df3 = rescale_columns_0_to_1(df2)

    flip_columns_so_1_is_always_best(df3, school_type)

    # Assume gaps in the data score 0
    # NaN -> 0
    df3 = df3.fillna(0)

    calculate_score(df3)
    return df3

def calculate_is_area_suitable(df, lower_site_req, upper_site_req):
    df['area_suitable'] = \
        (df['geoattributes.AREA'] > lower_site_req) & \
        (df['geoattributes.AREA'] < upper_site_req)

def z_score_scaling(df):
    '''Given inputs as rows of a dataframe, for every given column (apart from
    'area_suitable'), this function scales the values to a z-score and stores
    them in new columns '<column>_zscore'.
    '''
    for col in df.columns:
        if col == 'area_suitable':
            continue
        col_zscore = col + '_zscore'
        # zscore calculation: x = (x - column_mean)/column_stdev
        col_mean_normalized = df[col] - df[col].mean()
        standard_deviation = df[col].std(ddof=0)
        if standard_deviation == 0.0:
            # can't divide by zero
            df[col_zscore] = col_mean_normalized
        else:
            df[col_zscore] = col_mean_normalized / standard_deviation


def rescale_columns_0_to_1(df):
    return df.apply(
        lambda x: (x.astype(float) - min(x)) / ((max(x) - min(x)) or 0.1),
        axis=0)


def flip_columns_so_1_is_always_best(df, school_type):
    '''Given inputs as rows of a dataframe, scaled 0 to 1, flip value of
    particular columns, so that 1 is always means a positive thing and 0
    negative. Changes the df in-place.'''
    ideal_values = dict([
        ('area_suitable', 1),
        ('geoattributes.BROADBAND', 1),
        ('geoattributes.COVERAGE BY GREENBELT', 0),
        ('geoattributes.DISTANCE TO BUS STOP', 0),
        ('geoattributes.DISTANCE TO METRO STATION', 0),
        ('geoattributes.DISTANCE TO MOTORWAY JUNCTION', 1),
        ('geoattributes.DISTANCE TO OVERHEAD LINE', 1),
        ('geoattributes.DISTANCE TO PRIMARY SCHOOL',
            0 if school_type == 'secondary_school' else 1),
        ('geoattributes.DISTANCE TO RAIL STATION', 0),
        ('geoattributes.DISTANCE TO SECONDARY SCHOOL',
            0 if school_type == 'primary_school' else 1),
        ('geoattributes.DISTANCE TO SUBSTATION', 1),
        ])
    missing_ideal_values = set(df.columns) - set(ideal_values)
    assert not missing_ideal_values
    columns_to_flip = [col for col, ideal_value in ideal_values.items()
                       if ideal_value == 0]
    for col in columns_to_flip:
        df[col] = df[col].map(lambda x: 1.0 - x)

def calculate_score(df):
    '''Given inputs as rows of a dataframe, that are scaled 0 to 1, this
    function appends a column 'score' for ranking. (Score: bigger=better)
    '''
    df['score'] = np.linalg.norm(df, axis=1)
