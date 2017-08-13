from django.conf.urls import url, include
from navalny_live.views import (
    ListShowsView, PushSubscribe, PushUnsubscribe
)

urlpatterns = [
    url(
        r'^shows/$',
        ListShowsView.as_view(),
        name='shows_list'
    ),
    url(
        r'^push_service/', include([
            url(
                r'^subscribe/$',
                PushSubscribe.as_view(),
                name='subscribe'
            ),
            url(
                r'^unsubscribe/$',
                PushUnsubscribe.as_view(),
                name='unsubscribe'
            )
        ])
    )
]
