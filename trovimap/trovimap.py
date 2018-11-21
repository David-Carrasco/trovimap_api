import requests
import json
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

    # Request config
    headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'}

    # TODO - param_name is adapted until properties endpoint unifies the param_name for Neighborhood:
    #        (SublocalityId vs SubLocalityId)
    payload = ({'SubLocalityId': location_id}
               if isinstance(location, Neighborhood)
               else {location.param_name: location_id})

    r = requests.post(MAP_SHAPE_URL, headers=headers, data=json.dumps(payload))

    return r.json()






