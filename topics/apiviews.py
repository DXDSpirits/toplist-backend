from django.db import connection
from rest_framework.decorators import link
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from topics.models import Topic, Candidate
from topics.serializers import TopicSerializer, CandidateSerializer, VoteSerializer
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
            start = random.randint(0, count - 100)
            step = random.randint(1, 5)
            object_list = self.queryset[start:start + 10 * step:step]
        page = self.paginate_queryset(object_list)
        if page is not None:
            serializer = self.get_pagination_serializer(page)
        else:
            serializer = self.get_serializer(object_list, many=True)
        return Response(serializer.data)


    @link()
    def vote_times(self, request, pk=None):
        cursor = connection.cursor()
        query = 'select topic_id as topic,candidate1_id as condidate1,candidate2_id as condidate2 ,count(*) as times ' \
                'from topics_vote ' \
                'where topic_id=%s ' \
                'group by candidate1_id , candidate2_id' % int(pk)
        cursor.execute(query)
        desc = cursor.description
        result = [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
        ]
        cursor.close()
        return Response(result)


class CandidateViewSet(ReadOnlyModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    paginate_by = 10


class VoteCreation(CreateAPIView):
    permission_classes = []
    serializer_class = VoteSerializer

    def post_save(self, obj, created):
        pass