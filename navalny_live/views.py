from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Show
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