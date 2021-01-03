from django.urls import path, re_path
from . import views

app_name = 'patikeapp'
urlpatterns = [
    path('', views.index, name='index'),
    path('patike/', views.patike, name='patike'),
    path('patika/<int:id>', views.patika, name='patika'),
    path('patika/edit/<int:id>/', views.edit, name='edit'),
    path('new/', views.new, name='new')
]
