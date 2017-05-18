import pandas as pd
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
    '''Return the expected floor space (m^2) for the given parameters'''
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

def score_results(result_dicts, lower_site_req, upper_site_req, school_type):
    from pandas.io.json import json_normalize
    df = json_normalize(result_dicts)  # result_dicts was 'e' in ola
    df.apply(lambda x: pd.to_numeric(x, errors='ignore'))
    df.fillna(0)
    df['geoattributes.BROADBAND'] = \
        pd.to_numeric(df['geoattributes.BROADBAND'], errors='ignore')
    df['area_suitable'] = \
        (df['geoattributes.AREA'] > lower_site_req) & \
        (df['geoattributes.AREA'] < upper_site_req)

    cols = [
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
        'geoattributes.DISTANCE TO SUBSTATION']
    df2 = pd.concat([df[col] for col in cols], axis=1)

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
        for col in cols:
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

    df2['geoattributes.COVERAGE BY GREENBELT'].fillna(0, inplace=True)

    # Rescale minimum = 0 and maximum = 1 for each column
    df3 = df2.apply(
        lambda x: (x.astype(float) - min(x)) / ((max(x) - min(x)) or 0.1),
        axis=0)
    df3['geoattributes.COVERAGE BY GREENBELT'].fillna(0, inplace=True)

    # flip value of some columns, so that 1 is always positive and 0 negative
    ideal_values = dict([
        ('area_suitable', 1),
        ('geoattributes.BROADBAND', 1),
        ('geoattributes.COVERAGE BY GREENBELT', 0),
        ('geoattributes.DISTANCE TO BUS STOP', 1),
        ('geoattributes.DISTANCE TO METRO STATION', 1),
        ('geoattributes.DISTANCE TO MOTORWAY JUNCTION', 0),
        ('geoattributes.DISTANCE TO OVERHEAD LINE', 0),
        ('geoattributes.DISTANCE TO PRIMARY SCHOOL',
            1 if school_type == 'secondary_school' else 0),
        ('geoattributes.DISTANCE TO RAIL STATION', 1),
        ('geoattributes.DISTANCE TO SECONDARY SCHOOL',
            1 if school_type == 'primary_school' else 0),
        ('geoattributes.DISTANCE TO SUBSTATION', 0),
        ])
    missing_ideal_values = set(df3.columns) - set(ideal_values)
    assert not missing_ideal_values
    columns_to_flip = [col for col, ideal_value in ideal_values.items()
                       if ideal_value == 0]
    for col in columns_to_flip:
        df3[col] = df3[col].map(lambda x: 1.0 - x)

    # score
    df3['score'] = np.linalg.norm(df3, axis=1)

    # bundle up the score and search result
    df_final = json_normalize(result_dicts)
    df_final = pd.concat([df_final, df3[['score']], df[['area_suitable']]],
                         axis=1)
    return df_final
