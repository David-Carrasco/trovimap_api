import requests
import json
import itertools
#import glom


###############
### CLASSES ###
###############

class Location:

    # TODO: @property

    def __init__(self, name):
        self.name = name

class City(Location):

    def __init__(self, name):
        self.param_name = PARAM_NAME_CITY
        self.type_id = TYPE_ID_CITY
        super().__init__(name)


class Neighborhood(Location):

    def __init__(self, name):
        self.param_name = PARAM_NAME_NEIGHBORHOOD
        self.type_id = TYPE_ID_NEIGHBORHOOD
        super().__init__(name)


#################
### CONSTANTS ###
#################

#URLs

LOCATION_TEXT_URL = 'https://www.trovimap.com/api/v2/property/search'
LOCATION_SEO_URL = 'https://www.trovimap.com/api/v2/seo/view'
MAP_SHAPE_URL = 'https://www.trovimap.com/api/v2/map/shape'

#Configuration identities

PARAM_NAME_CITY = 'LocalityId'
TYPE_ID_CITY = 15

PARAM_NAME_NEIGHBORHOOD = 'SublocalityId'
TYPE_ID_NEIGHBORHOOD = 25


##################
### FUNCTIONS  ###
##################


# UTILS

def request_page(url, payload_base, default_page_param='Page'):

    # Request by page number
    for page in itertools.count(1):

        # Updating page parameter
        payload_base.update({default_page_param: page})

        # Request
        r = requests.post(url=url, data=json.dumps(payload_base))

        yield r.json()


# MAIN API

def get_search_location(location_name):
    '''
    :param location_name:
    :return:
    '''

    payload = {'searchString': location_name}
    r = requests.get(LOCATION_TEXT_URL, params=payload)

    return r.json()


def get_location_by_text(location):

    payload = {'type': location.type_id, 'text': location.name}
    r = requests.get(LOCATION_SEO_URL, params=payload)

    return r.json()


def get_properties_by_location(location):

    # Get location id for the param_name attribute
    location_id = get_location_by_text(location)[location.param_name]

    # TODO - param_name is adapted until properties endpoint unifies the param_name for Neighborhood:
    #        (SublocalityId vs SubLocalityId)
    payload = ({'SubLocalityId': location_id}
               if isinstance(location, Neighborhood)
               else {location.param_name: location_id})

    # Adding specific payload parameters for this endpoint
    payload.update({'PageSize': 20, 'Precision': 5, 'SortField': '_VisualScore'})

    # Getting properties ids in paginated requests until there is no properties
    properties = []
    for content in itertools.takewhile(lambda response: len(response['properties']),
                                       request_page(url=MAP_SHAPE_URL, payload_base=payload)):

        properties.append([property['Sysid'] for property in content['properties']])

    # Flatting properties lists
    properties = list(itertools.chain.from_iterable(properties))

    return properties

