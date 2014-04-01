
from django.conf.urls import patterns, include, url
from rest_framework import routers
from topics.apiviews import TopicViewSet

router = routers.DefaultRouter()

router.register(r'topic', TopicViewSet)

urlpatterns = patterns('',
    url(r'^', include(router.urls)),
)
