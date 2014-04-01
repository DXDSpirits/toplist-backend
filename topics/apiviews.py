from rest_framework.viewsets import ReadOnlyModelViewSet
from topics.models import Topic
from topics.serializers import TopicSerializer

class TopicViewSet(ReadOnlyModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    paginate_by = 10
