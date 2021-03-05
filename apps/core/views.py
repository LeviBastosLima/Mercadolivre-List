from typing import Union

from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy


def root(request) -> Union[HttpResponsePermanentRedirect, HttpResponseRedirect]:
    return redirect(reverse_lazy('sales:list_users_and_publications'))
