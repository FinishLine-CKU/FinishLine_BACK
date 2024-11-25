from django.urls import path
from . import views
from .views import signup_step1,signup_step2,login,logout
urlpatterns = [
    path('login/', login, name='login'),
    path('signup/step1/', signup_step1, name='signup_step1'),
    path('signup/step2/', signup_step2, name='signup_step2'),
    path('logout/',logout, name='logout'),
]
