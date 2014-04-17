
from django.conf.urls import patterns, include, url
from rest_framework import routers
from lovemessages.apiviews import MessageViewSet

router = routers.DefaultRouter()

router.register(r'message', MessageViewSet)

urlpatterns = patterns('',
    url(r'^', include(router.urls)),
)
