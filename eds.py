# -*- coding: utf-8 -*-

"""
Total credit to:
    - https://github.com/hectorcorrea
    - https://github.com/Brown-University-Library/bul-search/blob/1b2a8be9cf3d02c90145d43caf5416186ed64ba9/app/models/eds.rb
(not yet working)
"""

import json, logging, os
import requests


logging.basicConfig(
    level=logging.DEBUG )
log = logging.getLogger(__name__)
log.debug( 'logger ready!' )


class EDS( object ):

    def __init__( self ):
        self.base_url = 'https://eds-api.ebscohost.com'
        self.profile_id = os.environ['EDS_PROFILE_ID']
        self.credentials = {
            'UserId': os.environ['EDS_USER_ID'],
            'Password': os.environ['EDS_PASSWORD'],
            'InterfaceId': self.profile_id }
        self.auth_token = None
        self.auth_timeout = None
        self.session_token = None

    def search( self, text ):
        url = self.base_url + '/edsapi/publication/Search?query=#{text}&resultsperpage=20&pagenumber=1&sort=relevance&highlight=n&includefacets=y&view=brief&autosuggest=n'
        headers = {
            'x-authenticationToken': self.prep_auth_token(), 'x-sessionToken': self.prep_session_token() }
        r = requests.post( url, headers=headers )
        output = r.content
        log.debug( output )
        return output

    def prep_auth_token( self ):
        # TODO: make sure the token still is valid (via AuthTimeout in response)
        if not self.auth_token:
            log.debug( 'prepping auth_token' )
            url = self.base_url + '/authservice/rest/UIDAuth'
            data = json.dumps( self.credentials )
            r = requests.post( url, data=data )
            rdct = json.loads( r.content )
            self.auth_token = rdct['AuthToken']
            self.auth_timeout = rdct['AuthTimeout']
        return self.auth_token

    def prep_session_token( self ):
        if not self.session_token:
            log.debug( 'prepping session_token' )
            url = self.base_url + '/edsapi/rest/CreateSession?profile=#{@profile_id}&guest=n'
            headers = { 'x-authenticationToken': self.auth_token() }
            r = requests.get( url, headers=headers )
            rdct = json.loads( r.content )
            self.session_token = rdct['SessionToken']
        return self.session_token

    # end class EDS()
