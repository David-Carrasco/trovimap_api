# -*- coding: utf-8 -*-

from .context import trovimap
import unittest


class ApiTests(unittest.TestCase):
    """API base test cases"""


    def test_get_search_location_city(self):

        city = trovimap.City('Badalona')
        city_request = trovimap.get_location_by_text(location=city)

        self.assertIn(city.param_name, city_request.keys())
        self.assertEqual(city_request['Type'], trovimap.TYPE_ID_CITY)


    def test_get_search_location_neighborhood(self):

        neighborhood = trovimap.Neighborhood('Pacifico')
        neighborhood_request = trovimap.get_location_by_text(location=neighborhood)

        self.assertIn(neighborhood.param_name, neighborhood_request.keys())
        self.assertEqual(neighborhood_request['Type'], trovimap.TYPE_ID_NEIGHBORHOOD)


if __name__ == '__main__':
    unittest.main()


