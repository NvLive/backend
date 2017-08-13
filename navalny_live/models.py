from django.db import models


class AbstractDateTimeModel(models.Model):
    start_date = models.DateTimeField(
        default=None,
        blank=True, null=True
    )
    end_date = models.DateTimeField(
        default=None,
        blank=True, null=True
    )

    class Meta:
        abstract = True


class AbstractPlaceholderURL(models.Model):
    placeholder_image_url = models.URLField(
        default='',
        max_length=255,
        blank=True, null=True
    )

    class Meta:
        abstract = True


class Show(AbstractPlaceholderURL):
    title = models.CharField(
        max_length=255
    )
    description = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Show'
        verbose_name_plural = 'Shows'


class Broadcast(AbstractDateTimeModel, AbstractPlaceholderURL):
    title = models.CharField(
        max_length=255,
        verbose_name='Title'
    )
    description = models.TextField(
        verbose_name='Description'
    )
    transcript = models.TextField(
        verbose_name='Transcript'
    )
    contents = models.TextField(
        verbose_name='Content'
    )
    stream_url = models.CharField(
        # URLField wont allow rtmp scheme
        max_length=255,
        verbose_name='Stream URL'
    )
    youtube_url = models.URLField(
        max_length=255,
        verbose_name='YouTube URL'
    )
    is_live = models.BooleanField(
        default=False
    )
    is_featured = models.BooleanField(
        default=False
    )
    shows = models.ForeignKey(
        'navalny_live.Show',
        related_name='show_broadcast',
        verbose_name='Show of broadcast messages'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Broadcast'
        verbose_name_plural = 'Broadcasts'


class PushTokens(models.Model):
    token = models.CharField(
        max_length=255
    )
    shows = models.ManyToManyField(
        Show,
        related_name='shows_push_token',
        related_query_name='shows_push_token_rel',
        blank=True, null=True
    )

    def __str__(self):
        return self.token

    class Meta:
        verbose_name = 'PushToken'
        verbose_name_plural = 'PushTokens'
