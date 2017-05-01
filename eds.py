# -*- coding: utf-8 -*-

"""
Total credit to:
    - <https://github.com/hectorcorrea>
    - <https://github.com/Brown-University-Library/bul-search/blob/1b2a8be9cf3d02c90145d43caf5416186ed64ba9/app/models/eds.rb>
Other useful info:
    - <https://eds-api.ebscohost.com/AuthService/rest/help>
    - <https://eds-api.ebscohost.com/Console>
    - <http://edswiki.ebscohost.com/EDS_API_Documentation>
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
        self.auth_credentials = {
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
        if not self.auth_token:
            url = self.base_url + '/authservice/rest/UIDAuth'
            req_headers = { 'Accept': 'application/json', 'Content-Type':'application/json' }
            req_data = json.dumps( self.auth_credentials )
            r = requests.post( url, headers=req_headers, data=req_data )
            rdct = json.loads( r.content )
            self.auth_token = rdct['AuthToken']
            self.auth_timeout = rdct['AuthTimeout']
            log.debug( 'self.auth_token, ```{tkn}```; self.auth_timeout, ```{tmt}```'.format( tkn=self.auth_token, tmt=self.auth_timeout ) )
        return self.auth_token

    def prep_session_token( self ):
        if not self.session_token:
            log.debug( 'prepping session_token' )
            url = self.base_url + '/edsapi/rest/CreateSession'
            req_headers = { 'x-authenticationToken': self.auth_token, 'Accept': 'application/json', 'Content-Type':'application/json' }
            req_params = { 'profile': self.profile_id, 'guest': 'n' }
            r = requests.get( url, headers=req_headers, params=req_params )
            rdct = json.loads( r.content )
            self.session_token = rdct['SessionToken']
            log.debug( 'session_token, ```{}```'.format(session_token) )
        return self.session_token

    # def prep_session_token( self ):
    #     if not self.session_token:
    #         log.debug( 'prepping session_token' )
    #         url = self.base_url + '/edsapi/rest/CreateSession?profile=#{}&guest=n'.format( self.profile_id )
    #         log.debug( 'session_token url, ```{}```'.format(url) )
    #         headers = { 'x-authenticationToken': self.auth_token }
    #         r = requests.get( url, headers=headers )
    #         log.debug( 'session_token response, ```{}```'.format(r.content) )
    #         rdct = json.loads( r.content )
    #         self.session_token = rdct['SessionToken']
    #     return self.session_token

    # end class EDS()


if __name__ == '__main__':
    eds = EDS()
    result = eds.search( 'zen' )
    log.debug( 'result, ```{}```'.format(result) )
