from rest_framework import serializers
from .models import Show, Broadcast


class BroadcastSerializer(serializers.ModelSerializer):

    class Meta:
        model = Broadcast
        fields = ('id', 'title',)


class ShowSerializer(serializers.ModelSerializer):

    broadcasts = serializers.SerializerMethodField()

    @staticmethod
    def get_broadcasts(obj):
        return BroadcastSerializer(obj.broadcasts, many=True).data

    class Meta:
        model = Show
        fields = ('id', 'title', 'description', 'broadcasts')
