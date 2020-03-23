from django.conf.urls import url
from ..views import (CakeListView, CakeCreateView, CakeDetailView,
                     CakeUpdateView, CakeDeleteView)
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^create/$',  # NOQA
        login_required(CakeCreateView.as_view()),
        name="cake_create"),

    url(r'^(?P<pk>\d+)/update/$',
        login_required(CakeUpdateView.as_view()),
        name="cake_update"),

    url(r'^(?P<pk>\d+)/delete/$',
        login_required(CakeDeleteView.as_view()),
        name="cake_delete"),

    url(r'^(?P<pk>\d+)/$',
        CakeDetailView.as_view(),
        name="cake_detail"),

    url(r'^$',
        CakeListView.as_view(),
        name="cake_list"),
]
