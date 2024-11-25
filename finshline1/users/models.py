from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    # 추가 정보 설정 필드
    CHOICES = [
        ('double', '복수전공'),
        ('linked', '연계정공'),
        ('etc', '해당없음'),
    ]
    additional_major_type = models.CharField(max_length=10, choices=CHOICES, blank=True, null=True)
    
    SUB_MAJOR_CHOICES = [
        ('ai', 'AI 전공'),
        ('bio', '생명공학 전공'),
        ('business', '경영학 전공'),
        ('design', '디자인 전공'),
        ('etc', '해당없음'),
    ]
    sub_major = models.CharField(max_length=50, choices=SUB_MAJOR_CHOICES, blank=True, null=True)  # 드롭다운 값

    student_id = models.CharField(max_length=10, unique=True, null=True, blank=True)  # 학번
    department = models.CharField(max_length=100, null=True, blank=True)  # 학과
    real_name = models.CharField(max_length=100, null=True, blank=True)  # 이름

    USERNAME_FIELD = 'student_id'  # 학번을 인증에 사용
    REQUIRED_FIELDS = []  # 추가 필수 필드 없음

    def __str__(self):
        return self.real_name
