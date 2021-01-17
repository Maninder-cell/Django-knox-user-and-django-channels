from django.urls import path,include
import rest.views as views
from rest_framework.routers import DefaultRouter
#from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path("", views.api_root,name="main"),
    path("todo/",views.todoData.as_view({'get': 'list',
    'post': 'create'}),name="todo"),
    path("todo/<slug:owner>/",views.todoData.as_view({'get': 'list',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'},name="user_todo")),
    path("todo/<int:pk>/",views.todoData.as_view({'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'}), name="todo_detail"),
    path("users/",views.userData.as_view({'get': 'list'}),name="users"),
    path("users/<int:pk>/",views.todoData.as_view({'get': 'retrieve'}),name="user_detail")
]
