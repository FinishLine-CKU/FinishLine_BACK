from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

# Create your models here.
class CustomUser(AbstractUser):
    # 기본 사용자 필드
    student_id = models.CharField(max_length=10, unique=True)  # 학번
    department = models.CharField(max_length=100)             # 학과

    # 복수/부/연계전공 드롭다운 옵션
    MAJOR_CHOICES = [
        ('double', '복수전공'),
        ('minor', '부전공'),
        ('linked', '연계전공'),
        ('none', '해당 없음'),
    ]
    major_choice = models.CharField(
        max_length=100,
        choices=MAJOR_CHOICES,
        default='none',
    )

    # 소단위 전공 
    SUB_MAJOR_CHOICES = [
        ('science', '과학 전공'),
        ('arts', '예술 전공'),
        ('engineering', '공학 전공'),
        ('business', '경영 전공'),
        ('none', '해당 없음'),
    ]
    sub_major_choice = models.CharField(
        max_length=100,
        choices=SUB_MAJOR_CHOICES,
        default='none',
    )

    def __str__(self):
        return self.username
    
class UploadedPDF(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/pdfs/')
    extracted_text = models.TextField(blank=True, null=True)  # PDF에서 추출된 텍스트
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.file.name}"