import json
from django.db import connection
from django.utils import simplejson
from rest_framework import status
from rest_framework.decorators import link, action
from rest_framework.generics import CreateAPIView
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.viewsets import ReadOnlyModelViewSet
from topics.models import Topic, Candidate, Comment
from topics.serializers import TopicSerializer, CandidateSerializer, VoteSerializer, CommentSerializer
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

    @action(methods=['post', 'get'])
    def comment(self, request, pk=None):
        if request.method == 'POST':
            request.DATA['topic'] = pk
            serializer = CommentSerializer(data=request.DATA)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            comments = Comment.objects.all().filter(topic=self.get_object()).order_by('-id')[:100]
            return Response(CommentSerializer(comments, context={'request': request}, many=True).data)


class CandidateViewSet(ReadOnlyModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    paginate_by = 10

    @action(methods=['post'])
    def like(self, request, pk=None):
        candidate = self.get_object()
        candidate.like()
        return Response(CandidateSerializer(candidate, context={'request': request}).data)


class VoteCreation(CreateAPIView):
    permission_classes = []
    serializer_class = VoteSerializer

    def post_save(self, obj, created):
        pass