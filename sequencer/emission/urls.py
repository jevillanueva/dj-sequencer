from django.urls import path, re_path
from . import views

app_name = 'emissions'
urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.new, name='new'),
    re_path(r'^(?P<id>[0-9a-f-]{36})/new/$', views.new, name='new_by_department'),
    re_path(r'^(?P<id>[0-9a-f-]{36})/edit/$', views.edit, name='edit'),
    path('admin/', views.admin_index, name='admin_index'),
    re_path(r'^admin/(?P<id>[0-9a-f-]{36})/receive/$', views.admin_receive, name='admin_receive'),
    re_path(r'^admin/(?P<id>[0-9a-f-]{36})/new/$', views.admin_new, name='admin_new_by_department'),
    re_path(r'^admin/(?P<id>[0-9a-f-]{36})/edit/$', views.admin_edit, name='admin_edit'),
]