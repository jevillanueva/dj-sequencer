from django.conf import settings
from django.urls import path, re_path
from django.conf.urls.static import static
from . import views

app_name = 'emissions'
urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^(?P<id>[0-9a-f-]{36})/new/$', views.new, name='new'),
    re_path(r'^(?P<id>[0-9a-f-]{36})/new_batch/$', views.new_batch, name='new_batch'),
    re_path(r'^(?P<id>[0-9a-f-]{36})/edit/$', views.edit, name='edit'),
    re_path(r'^(?P<id>[0-9a-f-]{36})/upload/$', views.upload, name='upload'),
    re_path(r'^(?P<id>[0-9a-f-]{36})/files/$', views.files, name='files'),
    re_path(r'^(?P<id>[0-9a-f-]{36})/files/(?P<idfile>[0-9a-f-]{36})/delete/$', views.delete_file, name='delete_file'),
    re_path(r'^(?P<id>[0-9a-f-]{36})/files/(?P<idfile>[0-9a-f-]{36})/download/$', views.download_file, name='download_file'),
    path('admin/', views.admin_index, name='admin_index'),
    re_path(r'^admin/(?P<id>[0-9a-f-]{36})/receive/$', views.admin_receive, name='admin_receive'),
    re_path(r'^admin/(?P<id>[0-9a-f-]{36})/new/$', views.admin_new, name='admin_new'),
    re_path(r'^admin/(?P<id>[0-9a-f-]{36})/new_batch/$', views.admin_new_batch, name='admin_new_batch'),
    re_path(r'^admin/(?P<id>[0-9a-f-]{36})/edit/$', views.admin_edit, name='admin_edit'),
    re_path(r'^admin/(?P<id>[0-9a-f-]{36})/upload/$', views.admin_upload, name='admin_upload'),
    re_path(r'^admin/(?P<id>[0-9a-f-]{36})/files/$', views.admin_files, name='admin_files'),
    re_path(r'^admin/(?P<id>[0-9a-f-]{36})/files/(?P<idfile>[0-9a-f-]{36})/delete/$', views.admin_delete_file, name='admin_delete_file'),
    re_path(r'^admin/(?P<id>[0-9a-f-]{36})/files/(?P<idfile>[0-9a-f-]{36})/download/$', views.admin_download_file, name='admin_download_file'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)