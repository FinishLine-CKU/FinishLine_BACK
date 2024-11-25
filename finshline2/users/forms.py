from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


# 회원가입 폼
class signupationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['real_name', 'student_id','department','additional_major_type', 'sub_major','password1', 'password2']


# 로그인 폼
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, label="아이디")
    password = forms.CharField(widget=forms.PasswordInput, label="비밀번호")
