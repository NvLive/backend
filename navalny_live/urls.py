from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from navalny_live.views import (
    ListShowsView, PushSubscribe, PushUnsubscribe, RetrieveShowView,
    ListBroadcastsView, RetrieveBroadcastView,
)

urlpatterns = [
    url(
        r'^shows/$',
        ListShowsView.as_view(),
        name='shows_list'
    ),
    url(
        r'^show/([0-9]+)$',
        RetrieveShowView.as_view(),
        name='show'
    ),
    url(
        r'^broadcasts/$',
        ListBroadcastsView.as_view(),
        name='broadcast_list'
    ),
    url(
        r'^broadcast/([0-9]+)/$',
        RetrieveBroadcastView.as_view(),
        name='broadcast'
    ),
    url(
        r'^broadcasts/current/$',
        ListBroadcastsView.as_view(current=1),
        name='broadcast_current'
    ),

    url(
        r'^broadcasts/show/([0-9]+)/last/([0-9]+)/$',
        ListBroadcastsView.as_view(),
        name='broadcasts_show'
    ),
    url(
        r'^broadcasts/last/([0-9]+)/$',
        ListBroadcastsView.as_view(),
        name='broadcasts_last'
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

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

