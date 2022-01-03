"""API Lookups"""
import logging
import requests


class APILookup:
    ############################################################
    # constructor
    ############################################################
    def __init__(self, postcode_api_url):

        self.postcode_api_url = postcode_api_url
        self.LOGGER = logging.getLogger(__name__)

    ############################################################
    # str
    ############################################################
    def __str__(self):

        return repr(self.postcode_api_url)

    ############################################################
    # Lookup postcode on API to get lat/long
    ############################################################

    def do_postcode_lookup(self, post_code):
        """Do API postcode lookup

        Keyword arguments:
        api_url -- URL for the API call
        post_code -- passed post code to lookup
        """

        try:
            data = ''
            lkp_url = self.postcode_api_url + str(post_code)

            resp = requests.get(url=lkp_url)
            data = resp.json()
            self.LOGGER.debug(data)

        except Exception as exrec:

            self.LOGGER.error("Error in do_postcode_lookup %s", str(exrec.data), exc_info=True)

        finally:
            return data
