from django.urls import path, re_path
from . import views

app_name = 'emissions'
urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.new, name='new'),
    re_path(r'^new/(?P<id>[0-9a-f-]{36})/$', views.new, name='new_by_department'),
    path('user_department', views.user_department, name='user_department'),
]