import requests


###############
### CLASSES ###
###############

class Location:

    # TODO: @property

    def __init__(self, name):
        self.name = name

class City(Location):

    def __init__(self, name):
        self.param_name = 'LocalityId'
        self.type_id = TYPE_ID_NEIGHBORHOOD
        super().__init__(name)


class Neighborhood(Location):

    def __init__(self, name):
        self.param_name = 'SubLocalityId'
        self.type_id = TYPE_ID_CITY
        super().__init__(name)


#################
### CONSTANTS ###
#################

#URLs

LOCATION_TEXT_URL = 'https://www.trovimap.com/api/v2/property/search'
LOCATION_SEO_URL = 'https://www.trovimap.com/api/v2/seo/view'

#Configuration identities
TYPE_ID_CITY = '25'
TYPE_ID_NEIGHBORHOOD = '15'


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

    return (r.json())


def get_location_by_text(location):

    payload = {'type': location.type_id, 'text': location.name}
    r = requests.get(LOCATION_SEO_URL, params=payload)

    return (r.json())




