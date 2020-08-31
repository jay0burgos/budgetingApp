from django.urls import path
from . import views



urlpatterns = [
    
    path('login', views.login),
    path('', views.splashPage ),
    path('log_out', views.logout),
    path('createNewUser', views.createNewUser),
   

]