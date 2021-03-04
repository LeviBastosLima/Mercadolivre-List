from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    path('users-publications/', views.list_users_and_publications, name='list_users_and_publications')
]
