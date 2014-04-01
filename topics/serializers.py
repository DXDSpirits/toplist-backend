
from topics.models import Topic, Candidate
from rest_framework import serializers


class CandidateSerializer(serializers.ModelSerializer):
    picture = serializers.Field(source='picture_fullpath')
    class Meta:
        model = Candidate
        fields = ('id', 'rank', 'title', 'description', 'picture')
        depth = 0


class TopicSerializer(serializers.ModelSerializer):
    picture = serializers.Field(source='picture_fullpath')
    candidates = CandidateSerializer(many=True, source='candidate_set')
    class Meta:
        model = Topic
        fields = ('id', 'title', 'description', 'candidates')
        depth = 0
