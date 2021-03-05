from django.http import HttpResponse
from django.shortcuts import render

from apps.integrations.free_market import FreeMarket


def list_users_and_publications(request) -> HttpResponse:
    """GET sales/users-publications/
    list top ten users and publications
    """
    free_market = FreeMarket()
    publications, users = free_market.get_users_and_publications()
    return render(request, 'sales/list_users_and_publications.html', {
        'users': users,
        'publications': publications
    })
