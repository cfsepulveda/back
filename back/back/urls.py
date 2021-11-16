from django.conf.urls import url

from back.controller.wily_controller import cohesion_analisys
from back.controller.wily_controller import complexity

urlpatterns = [
        url(r'^complexity/$', complexity),
        url(r'^cohesion/$', cohesion_analisys)
]
