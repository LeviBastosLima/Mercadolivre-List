from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from apps.integrations.oauth import Oauth


def oauth_free_market(request):
    oauth = Oauth()
    response = oauth.get_free_market_authorization()
    return response


def oauth_redirect(request):
    code = request.GET.get('code')
    oauth = Oauth()
    user_data = oauth.get_token(code)
    print(user_data)
    return render(request, 'accounts/oauth_redirect.html', {
        'response': user_data
    })
