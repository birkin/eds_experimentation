info
====

- python3 demo-code to connect to [EBSCO's](https://www.ebsco.com) [EDS-API](http://edswiki.ebscohost.com/EDS_API_Documentation)

- Total credit to [Hector Correa's](https://github.com/hectorcorrea) ruby [code](https://github.com/Brown-University-Library/bul-search/blob/1b2a8be9cf3d02c90145d43caf5416186ed64ba9/app/models/eds.rb)

- useful links:
    - <https://eds-api.ebscohost.com/AuthService/rest/help>
    - <https://eds-api.ebscohost.com/Console>
    - <http://edswiki.ebscohost.com/EDS_API_Documentation>

Usage:

    $ source ../env/bin/activate  # loads environmental variables
    >>> eds = EDS()
    >>> result = eds.search( 'zen' )

---
