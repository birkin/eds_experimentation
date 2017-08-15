# -*- coding: utf-8 -*-

""" python3 tests for eds_experimentation code

    Usage: $ python ./test.py  # all tests
           $ python ./test.py EDS_Test.test_string_search  # specific test

    Note: according to B.B., there is no plain 'HAY' location for an item.
    That's a bib-level location; all hay items should have a more specific location. """

import os, pprint, re, time, unittest
from urllib.parse import parse_qs, urlparse

from eds import EDS


class EDS_Test( unittest.TestCase ):
    """ Tests eds-api calls. """

    def setUp(self):
        self.eds = EDS()


    def tearDown(self):
        pass

    def test_string_search( self ):
        """ Checks for data returned by string search. """
        result_dct = self.eds.search( 'zen' )
        ## top-level keys
        self.assertEqual(
            ['SearchRequestGet', 'SearchResult'],
            sorted( result_dct.keys() )
            )
        ## `Get` keys
        self.assertEqual(
            ['QueryString', 'SearchCriteriaWithActions'],
            sorted( result_dct['SearchRequestGet'] )
            )
        ## `Result` keys
        self.assertEqual(
            ['AvailableCriteria', 'AvailableFacets', 'Data', 'Statistics'],
            sorted( result_dct['SearchResult'] )
            )
        ## `Result['Data']` keys
        self.assertEqual(
            ['RecordFormat', 'Records'],
            sorted( result_dct['SearchResult']['Data'] )
            )
        ## `Result['Data']['Records']` info
        records_lst = result_dct['SearchResult']['Data']['Records']
        self.assertEqual(
            20,
            len( records_lst )
            )
        self.assertEqual(
            ['FullTextHoldings', 'Header', 'Items', 'PLink', 'RecordInfo', 'ResultId'],
            sorted( records_lst[0].keys() )
            )
        ## `Result['Data']['Records'][0]['FullTextHoldings']` info
        full_text_holdings_entry = result_dct['SearchResult']['Data']['Records'][0]['FullTextHoldings'][0]
        self.assertEqual(
            ['CoverageDates', 'CoverageStatement', 'Databases', 'EmbargoDescription', 'EmbargoUnit', 'Facts', 'Name', 'URL'],
            sorted( full_text_holdings_entry.keys() )
            )
        ## `Result['Data']['Records'][0]['Header']` info
        record_header = result_dct['SearchResult']['Data']['Records'][0]['Header']
        self.assertEqual(
             ['IsSearchable', 'PublicationId', 'RelevancyScore', 'ResourceType'],  # ResourceType can be, eg, 'Book', 'Journal', 'Report', etc
            sorted( record_header.keys() )
            )



if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    unittest.main( verbosity=2, warnings='ignore' )  # python3; warnings='ignore' from <http://stackoverflow.com/a/21500796>
