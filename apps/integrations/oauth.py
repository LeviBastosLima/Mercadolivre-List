from typing import Union, Dict

from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import redirect

from decouple import config
import meli


class Oauth:
    _APP_ID: str = config('APP_ID')
    _SECRET_KEY: str = config('SECRET_KEY')
    _FREE_MARKET_API_URL: str = config('MERCADO_LIBRE_API_URL', default='https://api.mercadolibre.com/')
    _FREE_MARKET_AUTH_URL: str = config('FREE_MARKET_AUTH_URL', default='http://auth.mercadolibre.com.ar/')
    _FREE_MARKET_REDIRECT_URL: str = config('FREE_MARKET_REDIRECT_URL',
                                       default='http://localhost:8000/accounts/oauth/redirect/')

    configuration: meli.Configuration = meli.Configuration(
        host=_FREE_MARKET_AUTH_URL
    )

    def get_free_market_authorization(self) -> Union[HttpResponsePermanentRedirect, HttpResponseRedirect]:
        """Redirect to free_market authorization page
        """
        free_market_oauth_url = '{}authorization?response_type=code&client_id={}&redirect_uri={}' \
            .format(self._FREE_MARKET_AUTH_URL, self._APP_ID, self._FREE_MARKET_REDIRECT_URL)
        response = redirect(free_market_oauth_url)
        return response

    def get_token(self, code: str) -> Dict[str, Union[str, int]]:
        """Get the access_token of free_market
        """
        print(code)
        with meli.ApiClient() as api_client:
            api_instance = meli.OAuth20Api(api_client)
            grant_type = 'authorization_code'
            client_id = self._APP_ID
            client_secret = self._SECRET_KEY
            redirect_uri = self._FREE_MARKET_REDIRECT_URL
            code = code
            api_response = api_instance.get_token(grant_type=grant_type, client_id=client_id,
                                                  client_secret=client_secret, redirect_uri=redirect_uri, code=code)
            return api_response
