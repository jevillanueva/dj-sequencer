from django.urls import path
from . import views

app_name = 'emissions'
urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.new, name='new'),
    path('user_department', views.user_department, name='user_department'),
]