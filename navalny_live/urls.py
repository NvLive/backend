from django.conf.urls import url

from navalny_live.views import ListShowsView

urlpatterns = [
    url(
        r'^shows/$',
        ListShowsView.as_view(),
        name='shows_list'
    )
]
