
from django.conf.urls import *
from django.urls import path
from . import views
from .controllers import user,migrations

urlpatterns = (

    path('user_groups/<int:id>/delete/', views.user_groups_delete, name='user_groups-delete'),

    path('group_create/', views.group_create, name='group-create'),
    path('group/', views.group_list, name='group-list'),
    path('group/<int:id>/', views.group_details, name='group-details'),
    path('group/<int:id>/delete/', views.group_delete, name='group-delete'),
    
    path('', views.home, name='home'),

    path('user/', user.user_list, name='user'),
    path('user-list/', user.user_list, name='user-list'),
    path('staff-list/', user.staff_list, name='staff-list'),
    path('user/<int:id>/', user.user_details, name='user-details'),
    path('user/<int:id>/delete/', user.user_delete, name='user-delete'),
    path('user/<int:id>/edit/', user.user_edit, name='user-edit'),

    path('user/<int:user_id>/create_discourse_user', user.create_discourse_user, name='create_discourse_user'),
    path('user/<int:user_id>/activate', user.activate_user, name='activate_user'),
    path('user/<int:user_id>/deactivate', user.deactivate_user, name='deactivate_user'),
    path('create_user', user.create_user, name='create_user'),
    path('change_password', user.change_password, name='change_password'),

    path('user/<int:user_id>/change_password', user.change_user_password, name='change_user_password'),
    path('user/<int:user_id>/set_department/<int:group_id>', user.set_department, name='set_department'),
    path('user/<int:user_id>/unset_department>', user.unset_department, name='unset_department'),

    path('user/<int:user_id>/add_to_group/<int:group_id>', views.add_user_to_group, name='add_user_to_group'),
    path('user/<int:user_id>/delete_from_group/<int:group_id>', views.delete_user_from_group, name='delete_user_from_group'),

    path('import_groups', migrations.import_dgroups, name='import_dgroups'),
    path('import_users', migrations.import_users, name='import_users'),
    path('import_dgroup/<str:groupname>/<int:da_group_id>', migrations.import_dgroup, name='import_dgroup'),
    

    path('testisvaliduser', views.testisvaliduser, name='testisvaliduser'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('deactivate_inactives', views.deactivate_inactives, name='deactivate_inactives'),
    path('set_basic_group', views.set_basic_group, name='set_basic_group'),
    

    

    #path('discourse_sso/', views.discourse_sso, name='discourse_sso'),
    path('anmeldung/index.html', views.discourse_sso, name='anmeldung1'),
    path('anmeldung/', views.discourse_sso, name='anmeldung'),

    path('testpd/', views.testpd, name='testpd'),
    path('fix_users_email', migrations.fix_users_email, name='fix_users_email' ),
    path('init_set_departments', migrations.init_set_departments, name='init_set_departments' )

)
