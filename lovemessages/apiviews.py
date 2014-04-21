from rest_framework.viewsets import ModelViewSet
from lovemessages.models import Message
from lovemessages.serializers import MessageSerializer


class MessageViewSet(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    paginate_by = 100
    
    def get_queryset(self):
        queryset = self.queryset
        params = self.request.QUERY_PARAMS
        if params and 'site' in params:
            queryset = queryset.filter(site = params['site'])
        return queryset
