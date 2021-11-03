from django.conf.urls import url

from back.controller.hello import hello_world
from back.controller.hello import cohesion_analisys
urlpatterns = [
    url(r'^hello/$', hello_world),
    url(r'^cohesion/$', cohesion_analisys)
]
