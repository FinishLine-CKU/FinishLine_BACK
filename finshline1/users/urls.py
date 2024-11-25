from django.urls import path
from . import views
from .views import signup_step1_view,signup_step2_view,login_view,logout_view
urlpatterns = [
    path('login/', login_view, name='login'),
    path('signup/step1/', signup_step1_view, name='signup_step1'),
    path('signup/step2/', signup_step2_view, name='signup_step2'),
    path('logout/',logout_view, name='logout'),
    
]
