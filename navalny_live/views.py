
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Show, PushTokens
from .serializers import ShowSerializer


class ListShowsView(ListAPIView):
    model = Show
    pagination_class = None
    permission_classes = [AllowAny]
    serializer_class = ShowSerializer

    def get_queryset(self):
        return self.model.objects.all()

    def get(self, request, *args, **kwargs):
        instances = self.get_queryset()
        for instance in instances:
            instance.broadcasts = instance.show_broadcast
        context = {'request': self.request}
        serializer = self.serializer_class(
            instance=instances, context=context, many=True
        )
        return Response(serializer.data)


class RetrieveShowView(RetrieveAPIView):
    model = Show

    def get(self, request, *args, **kwargs):
        instance_pk = kwargs['pk']
        pass


# Push token views
class PushSubscribe(CreateAPIView):
    model = PushTokens
    pagination_class = None
    permission_classes = [AllowAny]

    @staticmethod
    def ids_delimiter(value):
        if type(value) is int:
            return value
        else:
            if value[-1:] == ',':
                value = value[:-1]
            value = value.split(',')
            while ',' in value:
                value.remove(',')
            return value

    def post(self, request, *args, **kwargs):
        mobile_data = self.request.data
        token = mobile_data.get('token', None)
        show_ids = mobile_data.get('shows', None)
        if token is None or show_ids is None:
            return Response({'status': False}, status=404)
        if not self.model.objects.filter(token__icontains=token).exists():
            push_token = self.model.objects.create(**{'token': token})
        push_token = self.model.objects.filter(token__icontains=token).last()
        show_pks = self.ids_delimiter(show_ids)
        for show in Show.objects.filter(pk__in=show_pks):
            push_token.shows.add(show)
        return Response({})


class PushUnsubscribe(CreateAPIView):
    model = PushTokens
    pagination_class = None
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        mobile_data = self.request.data
        token = mobile_data.get('token', '')
        instance_qs = self.model.objects.filter(token__icontains=token)
        if not instance_qs.exists():
            return Response({}, status=404)
        instance_qs.delete()
        return Response({})
