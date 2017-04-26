from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^travels$', views.travels),
    url(r'^travels/add$', views.travels_add),
    url(r'^travels/add_process$', views.travels_add_process),
    url(r'^travels/join/(?P<travel_id>\d+)$', views.travel_join),
    url(r'^travels/destination/(?P<travel_id>\d+)$', views.travel_view),
    url(r'^logout$', views.logout),
]
