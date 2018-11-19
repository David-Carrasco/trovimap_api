# -*- coding: utf-8 -*-

from .context import trovimap
import unittest


class ApiTests(unittest.TestCase):
    """API base test cases"""


    def test_get_search_location_city(self):

        city = trovimap.City('Badalona')
        city_request = trovimap.get_location_by_text(location=city)

        #print(city_request['Type'])

        print(city_request)

        print(city_request.get('Type'))


        #self.assertIn(city.param_name, city_request.keys())
        self.assertEqual(city_request['Type'], trovimap.TYPE_ID_CITY)


    def test_get_search_location_neighborhood(self):

        neigborhood = trovimap.Neighborhood('Pacifico')
        neigborhood_request = trovimap.get_location_by_text(location=neigborhood)

        #self.assertIn(neigborhood.param_name, neigborhood_request.keys())
        self.assertEqual(neigborhood_request['Type'], trovimap.TYPE_ID_NEIGHBORHOOD)


if __name__ == '__main__':
    unittest.main()


