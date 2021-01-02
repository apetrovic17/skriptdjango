from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.index, name='patikeapp_index'),
    path('int/<br>', views.broj, name='patikeapp_broj')
]
