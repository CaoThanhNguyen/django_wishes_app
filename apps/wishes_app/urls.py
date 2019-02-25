from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^new$', views.new),
    url(r'^stats$', views.stats),
    url(r'^create$', views.create),
    url(r'^delete/(?P<wishId>\d+)$', views.delete),
    url(r'^edit/(?P<wishId>\d+)$', views.edit),
    url(r'^update/(?P<wishId>\d+)$', views.update),
    url(r'^granted/(?P<wishId>\d+)$', views.granted),
    url(r'^like/(?P<wishId>\d+)$', views.like),
]