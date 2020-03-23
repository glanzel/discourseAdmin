from django.conf.urls import url
from ..views import (BreadListView, BreadCreateView, BreadDetailView,
                     BreadUpdateView, BreadDeleteView)
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^create/$',  # NOQA
        login_required(BreadCreateView.as_view()),
        name="bread_create"),

    url(r'^(?P<pk>\d+)/update/$',
        login_required(BreadUpdateView.as_view()),
        name="bread_update"),

    url(r'^(?P<pk>\d+)/delete/$',
        login_required(BreadDeleteView.as_view()),
        name="bread_delete"),

    url(r'^(?P<pk>\d+)/$',
        BreadDetailView.as_view(),
        name="bread_detail"),

    url(r'^$',
        BreadListView.as_view(),
        name="bread_list"),
]
