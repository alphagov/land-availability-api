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

    # x-score scaling
    # (not really necessary because we scale it again, but useful for
    #  analysis)
    cols = [
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
    if False:
        for col in cols:
            col_zscore = col + '_zscore'
            col_mean_normalized = df[col] - df[col].mean()
            standard_deviation = df[col].std(ddof=0)
            if standard_deviation == 0.0:
                # can't divide by zero
                df[col_zscore] = col_mean_normalized
            else:
                df[col_zscore] = col_mean_normalized / standard_deviation

    # select columns we want to use for vector distance calculations
    # df.columns =
    # ['address',
    #  'authority',
    #  'centre.lat',
    #  'centre.lon',
    #  'footage',
    #  'geoattributes.AREA',
    #  'geoattributes.BROADBAND',
    #  'geoattributes.COVERAGE BY GREENBELT',
    #  'geoattributes.DISTANCE TO BUS STOP',
    #  'geoattributes.DISTANCE TO METRO STATION',
    #  'geoattributes.DISTANCE TO MOTORWAY JUNCTION',
    #  'geoattributes.DISTANCE TO OVERHEAD LINE',
    #  'geoattributes.DISTANCE TO PRIMARY SCHOOL',
    #  'geoattributes.DISTANCE TO RAIL STATION',
    #  'geoattributes.DISTANCE TO SECONDARY SCHOOL',
    #  'geoattributes.DISTANCE TO SUBSTATION',
    #  'geoattributes.FLOORSPACE',
    #  'id',
    #  'name',
    #  'owner',
    #  'postcode',
    #  'region',
    #  'structures',
    #  'uprn',
    #  'area_suitable',
    #  'geoattributes.BROADBAND_zscore',
    #  'geoattributes.COVERAGE BY GREENBELT_zscore',
    #  'geoattributes.DISTANCE TO BUS STOP_zscore',
    #  'geoattributes.DISTANCE TO METRO STATION_zscore',
    #  'geoattributes.DISTANCE TO MOTORWAY JUNCTION_zscore',
    #  'geoattributes.DISTANCE TO OVERHEAD LINE_zscore',
    #  'geoattributes.DISTANCE TO PRIMARY SCHOOL_zscore',
    #  'geoattributes.DISTANCE TO RAIL STATION_zscore',
    #  'geoattributes.DISTANCE TO SECONDARY SCHOOL_zscore',
    #  'geoattributes.DISTANCE TO SUBSTATION_zscore']
    #
    # [24:34]:
    # ['area_suitable',
    #  'geoattributes.BROADBAND_zscore',
    #  'geoattributes.COVERAGE BY GREENBELT_zscore',
    #  'geoattributes.DISTANCE TO BUS STOP_zscore',
    #  'geoattributes.DISTANCE TO METRO STATION_zscore',
    #  'geoattributes.DISTANCE TO MOTORWAY JUNCTION_zscore',
    #  'geoattributes.DISTANCE TO OVERHEAD LINE_zscore',
    #  'geoattributes.DISTANCE TO PRIMARY SCHOOL_zscore',
    #  'geoattributes.DISTANCE TO RAIL STATION_zscore',
    #  'geoattributes.DISTANCE TO SECONDARY SCHOOL_zscore']
    #df2 = df.iloc[:, 24:34]
    df2['geoattributes.COVERAGE BY GREENBELT'].fillna(0, inplace=True)

    # Rescale minimum = 0 and maximum = 1 for each column
    df3 = df2.apply(
        lambda x: (x.astype(float) - min(x)) / ((max(x) - min(x)) or 0.1),
        axis=0)
    df3['geoattributes.COVERAGE BY GREENBELT'].fillna(0, inplace=True)

    # create 'ideal' z-score
    df3['dist'] = df3.apply(lambda x: dist(x, school_type=school_type),
                            axis=1)
    df_final = json_normalize(result_dicts)
    df_final = pd.concat([pd.concat([df_final, df3[['dist']]], axis=1),
                          df[['area_suitable']]],
                         axis=1)
    return df_final

def dist(x, school_type):
    ''' Calculate the Euclidean distance from the 'ideal' values
    (in the 0-1 range).
    '''
    if school_type == 'secondary_school':
        ideal = (1, 0, 1, 1, 0, 1, 0, 0, 1, 1)
    elif school_type == 'primary_school':
        ideal = (1, 0, 1, 1, 0, 1, 1, 0, 0, 1)
    else:
        raise NotImplementedError

    df = pd.DataFrame(x)
    df_x = df.values
    from pprint import pprint
    print('Dist calculation:')
    print('df_x:')
    pprint(df_x)
    print('ideal:')
    pprint(ideal)
    print('df_x - ideal:')
    pprint(df_x - ideal)
    print('np.linalg.norm(df_x - ideal):')
    pprint(np.linalg.norm(df_x - ideal))
    import pdb; pdb.set_trace()
    # what about: np.linalg.norm(df_x - np.array([[v] for v in ideal]))
    return np.linalg.norm(df_x - ideal)

def clean_columns(columns):
    cols = list(columns)
    cols.remove('id')
    cols.remove('address')
    cols.remove('authority')
    cols.remove('centre.lat')
    cols.remove('centre.lon')
    cols.remove('name')
    cols.remove('owner')
    cols.remove('postcode')
    cols.remove('region')
    cols.remove('structures')
    cols.remove('footage')
    cols.remove('geoattributes.AREA')
    cols.remove('area_suitable')
    cols.remove('uprn')
    cols.remove('geoattributes.FLOORSPACE')
    return cols
