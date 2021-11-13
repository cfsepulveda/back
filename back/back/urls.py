from django.conf.urls import url

from back.controller.wily_controller import complexity

urlpatterns = [
        url(r'^complexity/$', complexity)
]
