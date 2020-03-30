
from django.conf.urls import *
from django.urls import path
from . import views

urlpatterns = (

    path('user_groups/', views.user_groups_list, name='user_groups-list'),
    path('user_groups/<int:id>/', views.user_groups_details, name='user_groups-details'),
    path('user_groups/<int:id>/delete/', views.user_groups_delete, name='user_groups-delete'),

    path('group/', views.group_list, name='group-list'),
    path('group/<int:id>/', views.group_details, name='group-details'),
    path('group/<int:id>/delete/', views.group_delete, name='group-delete'),
    path('user/', views.user_list, name='user-list'),
    path('user/<int:id>/', views.user_details, name='user-details'),
    path('user/<int:id>/delete/', views.user_delete, name='user-delete'),
    path('user/<int:id>/edit/', views.user_edit, name='user-edit'),
    path('import_groups', views.import_dgroups, name='import_dgroups'),
    path('import_users', views.import_users, name='import_users'),
    path('create_user', views.create_user, name='create_user'),

)
