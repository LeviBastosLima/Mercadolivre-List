from typing import Union

from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from apps.integrations.oauth import Oauth


def oauth_free_market(request) -> Union[HttpResponsePermanentRedirect, HttpResponseRedirect]:
    """GET oauth/free-market/
    """
    oauth = Oauth()
    response = oauth.get_free_market_authorization()
    print(response)
    return response


def oauth_redirect(request) -> HttpResponse:
    """GET oauth/redirect/
    """
    code = request.GET.get('code')
    print('request', request)
    print('code', code)
    oauth = Oauth()
    user_data = oauth.get_token(code)
    print(user_data)
    return render(request, 'accounts/oauth_redirect.html', {
        'response': user_data
    })
