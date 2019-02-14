import requests
import json
import itertools

#################
### CONSTANTS ###
#################

# URLs

LOCATION_TEXT_URL = 'https://www.trovimap.com/api/v2/property/search'
LOCATION_SEO_URL = 'https://www.trovimap.com/api/v2/seo/view'
MAP_SHAPE_URL = 'https://www.trovimap.com/api/v2/map/shape'

# Configuration identities

PARAM_NAME_CITY = 'LocalityId'
TYPE_ID_CITY = 15

PARAM_NAME_NEIGHBORHOOD = 'SublocalityId'
TYPE_ID_NEIGHBORHOOD = 25


###############
### CLASSES ###
###############

class Trovimap:

    def _get_location_by_name(self, location_name):

        payload = {'searchString': location_name}
        endpoint = Endpoint('_get_location_by_name', payload)

        return endpoint.request_get()

    def get_neighborhoods_by_city(self):
        pass  #TODO

    def get_city_details(self, city_name):

        payload = {'type': TYPE_ID_CITY, 'text': city_name}
        endpoint = Endpoint('get_location_details', payload)

        return endpoint.request_get()

    def get_neighborhood_details(self, neighborhood_name):

        payload = {'type': TYPE_ID_NEIGHBORHOOD, 'text': neighborhood_name}
        endpoint = Endpoint('get_location_details', payload)

        return endpoint.request_get()

    def get_properties_by_city(self, city_name):
        '''Get the property ids of a city'''

        location_id = self.get_city_details(city_name)[PARAM_NAME_CITY]
        payload = {PARAM_NAME_CITY: location_id, 'PageSize': 20, 'Precision': 5, 'SortField': '_VisualScore'}
        endpoint = Endpoint('get_properties', payload)

        # pagination generator
        properties_pagination = endpoint.request_post_pagination()

        # properties list
        properties = [[elem['Sysid'] for elem in property_elem['properties']]
                      for property_elem in
                      itertools.takewhile(lambda response: len(response['properties']), properties_pagination)]

        return list(itertools.chain.from_iterable(properties))


    def get_properties_by_neighborhood(self, neighborhood_name):
        '''Get the property ids of a neighborhood'''

        location_id = self.get_neighborhood_details(neighborhood_name)[PARAM_NAME_NEIGHBORHOOD]
        payload = {'SubLocalityId': location_id, 'PageSize': 20, 'Precision': 5, 'SortField': '_VisualScore'}
        endpoint = Endpoint('get_properties', payload)

        # pagination generator
        properties_pagination = endpoint.request_post_pagination()

        # properties list
        properties = [[elem['Sysid'] for elem in property_elem['properties']]
                      for property_elem in
                      itertools.takewhile(lambda response: len(response['properties']), properties_pagination)]

        return list(itertools.chain.from_iterable(properties))


class Endpoint:

    func_url = {
        '_get_location_by_name': LOCATION_TEXT_URL,
        'get_location_details': LOCATION_SEO_URL,
        'get_properties': MAP_SHAPE_URL
    }

    def __init__(self, func_name, payload):

         self._url = self.func_url.get(func_name)
         self._payload = payload

    def request_get(self):

        r = requests.get(self._url, params=self._payload)
        return r.json()

    def request_post_pagination(self):
        ''' Request by page number'''

        for page in itertools.count(1):

            self._payload.update({'Page': page})

            # Request
            r = requests.post(url=self._url, data=json.dumps(self._payload))

            yield r.json()



