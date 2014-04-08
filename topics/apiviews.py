from rest_framework.viewsets import ReadOnlyModelViewSet
from topics.models import Topic
from topics.serializers import TopicSerializer
from rest_framework.response import Response
import random

class TopicViewSet(ReadOnlyModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    paginate_by = 10
    
    def list(self, request, *args, **kwargs):
        object_list = self.queryset
        count = self.queryset.count()
        if count > 100:
            start = random.randint(0, count-100)
            step = random.randint(1, 5)
            object_list = self.queryset[start:start+10*step:step]
        page = self.paginate_queryset(object_list)
        if page is not None:
            serializer = self.get_pagination_serializer(page)
        else:
            serializer = self.get_serializer(object_list, many=True)
        return Response(serializer.data)
