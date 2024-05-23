from django.urls import path
from . import views

app_name = 'emission'
urlpatterns = [
    path('', views.index, name='index'),
]