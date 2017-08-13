from rest_framework import serializers
from .models import Show, Broadcast


class BroadcastSerializer(serializers.ModelSerializer):

    class Meta:
        model = Broadcast
        fields = ('id', 'title', 'transcript', 'contents', 'stream_url',
                  'youtube_url', 'is_live', 'is_featured', 'start_date',
                  'end_date', 'placeholder_image_url',)


class ShowSerializer(serializers.ModelSerializer):

    broadcasts = serializers.SerializerMethodField()

    @staticmethod
    def get_broadcasts(obj):
        try:
            return BroadcastSerializer(obj.broadcasts, many=True).data
        except Exception:
            return BroadcastSerializer(obj.broadcasts).data

    class Meta:
        model = Show
        fields = ('id', 'title', 'description', 'broadcasts',
                  'placeholder_image_url',)
