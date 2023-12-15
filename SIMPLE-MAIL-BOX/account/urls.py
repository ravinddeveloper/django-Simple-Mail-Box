from django.urls import path,include
from .views import *
urlpatterns = [
   path('login/',handle_login,name='login'),
   path('register/',register,name='register'),
   path('logout/',handle_logout,name='logout'),
   path('profile/',profile.as_view(),name='profile'),
   path('reset-password/',reset_password,name='reset_pass'),

]
