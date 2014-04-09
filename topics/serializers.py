from topics.models import Topic, Candidate, Vote
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _


class CandidateSerializer(serializers.ModelSerializer):
    picture = serializers.Field(source='picture_fullpath')
    score = serializers.IntegerField(source='score')
    vote_times = serializers.IntegerField(source='vote_times')

    class Meta:
        model = Candidate
        fields = ('id', 'rank', 'title', 'description', 'picture', 'score', 'vote_times')
        depth = 0


class TopicSerializer(serializers.ModelSerializer):
    picture = serializers.Field(source='picture_fullpath')
    candidates = CandidateSerializer(many=True, source='candidate_set')

    class Meta:
        model = Topic
        fields = ('id', 'title', 'description', 'candidates')
        depth = 0


class VoteSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    candidate1 = serializers.IntegerField(required=True)
    candidate2 = serializers.IntegerField(required=True)
    draw = serializers.IntegerField(required=True)
    topic = serializers.IntegerField(required=True)

    def save_object(self, obj, **kwargs):
        vote = Vote.objects.create(candidate1=Candidate.objects.get(id=obj.get('candidate1')),
                                   candidate2=Candidate.objects.get(id=obj.get('candidate2')),
                                   draw=obj.get('draw'),
                                   topic=Topic.objects.get(id=obj.get('topic')), )
        obj['id'] = vote.id

    def validate(self, attrs):
        candidate1 = Candidate.objects.get(id=attrs['candidate1'])
        candidate2 = Candidate.objects.get(id=attrs['candidate2'])
        topic_id = attrs['topic']
        if candidate1.topic.id == topic_id and candidate2.topic.id == topic_id:
            return attrs
        else:
            raise serializers.ValidationError(_("Topic and candidate don't match."))



