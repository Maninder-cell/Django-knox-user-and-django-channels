from django.urls import path,include
from .views import RegisterAPI,LogInApi,UserApi
from knox import views as knox_views

urlpatterns = [
    path("auth/",include("knox.urls")),
    path("auth/register/",RegisterAPI.as_view(),name="register"),
    path("auth/logIn/",LogInApi.as_view(),name="login"),
    path("auth/user/",UserApi.as_view(),name="current_user"),
    path("auth/logout/",knox_views.LogoutView.as_view(),name="logout"),
]