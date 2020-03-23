from django.conf.urls import include, url

app_name="baker"

urlpatterns = [

    url(r'^breads/', include('baker.urls.bread_urls')),  # NOQA
    url(r'^cakes/', include('baker.urls.cake_urls')),
]
