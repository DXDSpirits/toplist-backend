from rest_framework.viewsets import ModelViewSet
from lovemessages.models import Message
from lovemessages.serializers import MessageSerializer


class MessageViewSet(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    paginate_by = 10
