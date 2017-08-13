from datetime import datetime

from apns import Payload, PayloadAlert, APNs
from django.conf import settings
from django_rq import job
from redis import Redis
from rq_scheduler import Scheduler

from navalny_live.models import Show, PushTokens


class AbstractNotification(object):
    def to_apns(self):
        raise NotImplementedError()

    def to_fcm(self):
        raise NotImplementedError()


class NavalniPayload(object):
    """
    A custom class representing an APNs message payload for iOS10
    """
    __slots__ = ('badge', 'type', 'content', 'attachment_url',)

    def __init__(self, badge=None, type=None, content=None,
                 attachment_url=None):
        super(NavalniPayload, self).__init__()
        self.type = type
        self.badge = badge
        self.content = content
        self.attachment_url = attachment_url

    def dict(self):
        """
        Returns the payload as a regular Python dictionary
        """
        d = {}
        if self.type:
            d.update({'type': self.type})
        if self.badge:
            d.update({'badge': self.badge})
        if self.content:
            d.update({'content': self.content})
        if self.attachment_url:
            d.update({'attachment-url': self.attachment_url})
        d = {'data': d}
        return d

    def __repr__(self):
        attrs = ('badge', 'type', 'content', 'attachment_url',)
        args = ', '.join(['%s=%r' % (n, getattr(self, n))
                          for n in attrs if hasattr(self, n)])
        return '%s(%s)' % (self.__class__.__name__, args)


class CustomPayloadAlert(PayloadAlert):
    def __init__(self, body=None, action_loc_key=None, loc_key=None,
                 loc_args=None, launch_image=None, title=None, title_loc_key=None,
                 title_loc_args=None):
        super(CustomPayloadAlert, self).__init__(
            body=body, action_loc_key=action_loc_key,
            loc_key=loc_key, loc_args=loc_args, launch_image=launch_image)
        if title is not None:
            self.title = title
        if title_loc_key is not None:
            self.title_loc_key = title_loc_key
        if title_loc_args is not None:
            self.title_loc_args = title_loc_args

    def dict(self):
        d = super(CustomPayloadAlert, self).dict()
        if hasattr(self, 'title'):
            d['title'] = self.title
        if hasattr(self, 'title_loc_key'):
            d['title-loc-key'] = self.title_loc_key
        if hasattr(self, 'title_loc_args'):
            d['title-loc-args'] = self.title_loc_args
        return d


class RichNotification(AbstractNotification):
    PHOTO_MESSAGE_PUSH = 'PhotoMessage'

    def __init__(self, loc_key, badge, content=None,
                 sound=None, alert=None, as_dict=None):
        self.alert = alert
        self.as_dict = as_dict
        self.loc_key = loc_key
        self.content = content
        self.sound = sound if sound is not None else 'default'
        self.badge = int(badge) if badge is not None else None
        self.message = self.make_message(self.content)

    @staticmethod
    def make_message(obj):
        """
        :param obj: ShowSerializer
        :return: dict with data in param:data
        """
        from navalny_live.serializers import ShowSerializer
        return ShowSerializer(obj).data

    def append_data_to_content(self, data):
        """
        Check type of data and append it in some of types
        :param data: struct data for APNs
        :return: self.content
        """
        self.content = {}
        self.content.update(data)
        return self.content

    def __repr__(self):
        return '<RichNotification: {}'.format(self.loc_key)

    def to_apns(self):
        kwargs_alert, kwargs_payload = {}, {}
        self.content = self.append_data_to_content(self.message)
        barev_payload = NavalniPayload(content=self.content)
        kwargs_payload.update({'alert': self.alert, 'sound': self.sound})
        kwargs_payload.update({'custom': barev_payload.dict(), 'badge': 1})
        main_payload = Payload(**kwargs_payload)
        return main_payload.dict() if self.as_dict else main_payload

    def to_fcm(self):
        return {}


class SendPushiOS(object):
    """
    Class for notify user messages by APNS
    """

    KEYS_FILE = settings.MEDIA_ROOT + '/iphone_ck.pem'

    @staticmethod
    def get_server(use_sandbox=True, keys_file=KEYS_FILE):
        """
        Create and return production or develop server
        :param use_sandbox:
        :param keys_file:
        :return:
        """
        return APNs(use_sandbox=use_sandbox, cert_file=keys_file,
                    key_file=keys_file)

    @staticmethod
    def get_feedbacks(server):
        """
        Get inactive tokens
        :param server:
        :return:
        """
        return list(server.feedback_server.items())

    @job
    def notify_message(self, tokens):
        server = self.get_server()
        show = Show.objects.filter(show_broadcast__is_live=True).last()
        alert = CustomPayloadAlert(
            title=show.title, body=show.description)
        # TODO: Check here send payload with param: as_dict -> True/False
        push_notification = RichNotification(
            badge=1, content=show, sound='parampam.wav',
            alert=alert, loc_key='subscribe', as_dict=True
        )
        for token in tokens:
            return server.gateway_server.send_notification(
                payload=push_notification.to_apns(), token=token
            )


send_live = SendPushiOS
scheduler = Scheduler(connection=Redis())
scheduler.schedule(
    scheduled_time=datetime.utcnow(),
    func=send_live.notify_message,
    args=[PushTokens.objects.values_list('token', flat=True)],
    interval=360,
    repeat=None
)
