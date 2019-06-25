SCHEMA = {
    'events' : {
        'cameo-families': ['2', '3', '6', '7', '8', '9', '10', '11', '12',
                           '13', '14', '15', '16', '17', '18', '19', '20'],
        'aggressive-cameo-families': ['13', '14', '15', '16', '17', '18', '19', '20'],
        'columns-dtypes': {
            'globaleventid': 'int64',
            'day': 'int64',
            'monthyear': 'int64',
            'year': 'int64',
            'fractiondate': 'float64',
            'actor1code': 'object',
            'actor1name': 'object',
            'actor1countrycode': 'object',
            'actor1knowngroupcode': 'object',
            'actor1ethniccode': 'object',
            'actor1religion1code': 'object',
            'actor1religion2code': 'object',
            'actor1type1code': 'object',
            'actor1type2code': 'object',
            'actor1type3code': 'object',
            'actor2code': 'object',
            'actor2name': 'object',
            'actor2countrycode': 'object',
            'actor2knowngroupcode': 'object',
            'actor2ethniccode': 'object',
            'actor2religion1code': 'object',
            'actor2religion2code': 'object',
            'actor2type1code': 'object',
            'actor2type2code': 'object',
            'actor2type3code': 'object',
            'isrootevent': 'bool',
            'eventcode': 'int64',
            'eventbasecode': 'int64',
            'eventrootcode': 'int64',
            'quadclass': 'int64',
            'goldsteinscale': 'float64',
            'nummentions': 'int64',
            'numsources': 'int64',
            'numarticles': 'int64',
            'avgtone': 'float64',
            'actor1geo_type': 'float64',	### Float because NAs preclude Pandas treating it as int64
            'actor1geo_fullname': 'object',
            'actor1geo_countrycode': 'object',
            'actor1geo_adm1code': 'object',
            'actor1geo_lat': 'float64',
            'actor1geo_long': 'float64',
            'actor1geo_featureid': 'object',
            'actor2geo_type': 'float64',
            'actor2geo_fullname': 'object',
            'actor2geo_countrycode': 'object',
            'actor2geo_adm1code': 'object',
            'actor2geo_lat': 'float64',
            'actor2geo_long': 'float64',
            'actor2geo_featureid': 'object',
            'actiongeo_type': 'float64',
            'actiongeo_fullname': 'object',
            'actiongeo_countrycode': 'object',
            'actiongeo_adm1code': 'object',
            'actiongeo_lat': 'float64',
            'actiongeo_long': 'float64',
            'actiongeo_featureid': 'object',	### Seems to be alphanumeri
            'dateadded': 'int64',
            #'sourceurl': 'object'
        },
        'useful_cols': ['monthyear', 'year', 'actor1countrycode', 'actor2countrycode',
                        'eventrootcode', 'goldsteinscale', 'numsources', 'numarticles', 'avgtone']
    }
}
AGENT_DATA = {
    'stats_agents_id': '*',
    'full_data': '*FULL*',
    'aggressive_data': '*AGRR*',
    'main_agent': 'main'
}
STATS_DATA = {
    'scales': {'goldsteinscale', 'custom_coeff'},
    'kind_of_stat': {'trend_line', 'diplomacy'}
}
PLOT_DATA = {
    'full_data': 'All',
    'aggressive_data': 'Aggressive',
}