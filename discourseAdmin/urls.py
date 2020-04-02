
from django.conf.urls import *
from django.urls import path
from . import views

urlpatterns = (

    path('user_groups/<int:id>/delete/', views.user_groups_delete, name='user_groups-delete'),

    path('group/', views.group_list, name='group-list'),
    path('group/<int:id>/', views.group_details, name='group-details'),
    path('group/<int:id>/delete/', views.group_delete, name='group-delete'),
    path('', views.user_list, name='user-list'),
    path('user/', views.user_list, name='user-list'),
    path('user/<int:id>/', views.user_details, name='user-details'),
    path('user/<int:id>/delete/', views.user_delete, name='user-delete'),
    path('user/<int:id>/edit/', views.user_edit, name='user-edit'),
    path('import_groups', views.import_dgroups, name='import_dgroups'),
    path('import_users', views.import_users, name='import_users'),
    path('create_user', views.create_user, name='create_user'),
    path('user/<int:user_id>/add_to_group/<int:group_id>', views.add_user_to_group, name='add_user_to_group'),
    path('user/<int:user_id>/delete_from_group/<int:group_id>', views.delete_user_from_group, name='delete_user_from_group'),

)
