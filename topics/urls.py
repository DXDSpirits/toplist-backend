
from django.conf.urls import patterns, include, url
from rest_framework import routers
from topics.apiviews import TopicViewSet, CandidateViewSet, VoteCreation

router = routers.DefaultRouter()

router.register(r'topic', TopicViewSet)
router.register(r'candidate', CandidateViewSet)
urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^vote/', VoteCreation.as_view()),
)
