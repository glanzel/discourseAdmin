
from django.conf.urls import *
from django.urls import path
from . import views

urlpatterns = (

    path('user_groups/<int:id>/delete/', views.user_groups_delete, name='user_groups-delete'),

    path('group_create/', views.group_create, name='group-create'),
    path('group/', views.group_list, name='group-list'),
    path('group/<int:id>/', views.group_details, name='group-details'),
    path('group/<int:id>/delete/', views.group_delete, name='group-delete'),
    
    path('', views.home, name='home'),

    path('user/', views.user_list, name='user'),
    path('user-list/', views.user_list, name='user-list'),
    path('staff-list/', views.staff_list, name='staff-list'),
    path('user/<int:id>/', views.user_details, name='user-details'),
    path('user/<int:id>/delete/', views.user_delete, name='user-delete'),
    path('user/<int:id>/edit/', views.user_edit, name='user-edit'),

    path('import_groups', views.import_dgroups, name='import_dgroups'),
    path('import_users', views.import_users, name='import_users'),
    path('import_dgroup/<str:groupname>/<int:da_group_id>', views.import_dgroup, name='import_dgroup'),
    
    path('user/<int:user_id>/activate', views.activate_user, name='activate_user'),
    path('user/<int:user_id>/deactivate', views.deactivate_user, name='deactivate_user'),
    path('create_user', views.create_user, name='create_user'),
    path('change_password', views.change_password, name='change_password'),

    path('testisvaliduser', views.testisvaliduser, name='testisvaliduser'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('deactivate_inactives', views.deactivate_inactives, name='deactivate_inactives'),
    path('set_basic_group', views.set_basic_group, name='set_basic_group'),
    
    

    path('user/<int:user_id>/change_password', views.change_user_password, name='change_user_password'),
    path('user/<int:user_id>/add_to_group/<int:group_id>', views.add_user_to_group, name='add_user_to_group'),
    path('user/<int:user_id>/delete_from_group/<int:group_id>', views.delete_user_from_group, name='delete_user_from_group'),
    path('user/<int:user_id>/set_department/<int:group_id>', views.set_department, name='set_department'),
    path('user/<int:user_id>/unset_department>', views.unset_department, name='unset_department'),
    

    #path('discourse_sso/', views.discourse_sso, name='discourse_sso'),
    path('anmeldung/index.html', views.discourse_sso, name='anmeldung1'),
    path('anmeldung/', views.discourse_sso, name='anmeldung'),

    path('testpd/', views.testpd, name='testpd'),
    path('fix_users_email', views.fix_users_email, name='fix_users_email' ),
    path('init_set_departments', views.init_set_departments, name='init_set_departments' )

)
