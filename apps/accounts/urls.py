from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('oauth/free-market/', views.oauth_free_market, name='oauth_free_market'),
    path('oauth/redirect/', views.oauth_redirect, name='oauth_redirect')
]
