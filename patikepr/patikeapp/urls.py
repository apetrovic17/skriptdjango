from django.urls import path, re_path
from . import views
from django.conf.urls import url

app_name = 'patikeapp'
urlpatterns = [
    path('', views.index, name='index'),
    path('patike/', views.patike, name='patike'),
    path('patika/<int:id>', views.patika, name='patika'),
    path('patika/edit/<int:id>/', views.edit, name='edit'),
    path('new/', views.new, name='new'),
    url(r'^register/$', views.user_register, name='user_register'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('oceni/<int:id>', views.oceni, name='oceni')
]
