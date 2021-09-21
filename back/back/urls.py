from django.conf.urls import url

from back.controller.hello import hello_world

urlpatterns = [
    url(r'^hello/$', hello_world)
]
