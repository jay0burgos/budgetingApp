from django.urls import path
from . import views


urlpatterns = [
    path('createNewUser', views.createNewUser),
    path('login', views.login),
    path('', views.splashPage )
]