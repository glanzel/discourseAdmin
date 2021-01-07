"""dsso URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from discourseAdmin.admin import user_admin_site
#from discourse_django_sso import views

#from crudbuilder import urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('ua/', user_admin_site.urls),
    path(r'', include('discourseAdmin.urls')),

]

#urlpatterns += post_crud.get_url_patterns()

# urlpatterns = [
#     path(
#         'sso/',
#         views.SSOProviderView.as_view(
#             sso_redirect=settings.DISCOURSE_SSO_REDIRECT,
#             sso_secret=settings.DISCOURSE_SSO_KEY
#         ),
#         name="sso"
#     ),
# ] + urlpatterns



# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns = [
#         path('__debug__/', include(debug_toolbar.urls)),
# 
#         # For django versions before 2.0:
#         # url(r'^__debug__/', include(debug_toolbar.urls)),
# 
#     ] + urlpatterns
    
#print(urlpatterns);    
    
    
    
