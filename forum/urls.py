
from django.conf.urls import *
from django.urls import path
from . import views

urlpatterns = (
    path('forum/', views.forum_list, name='forum-list'),
    path('forum/<int:id>/', views.forum_details, name='forum-details'),
    path('forum/<int:id>/delete/', views.forum_delete, name='forum-delete'),
)
