from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

# Create your models here.
class CustomUser(AbstractUser):
    student_id = models.CharField(max_length=10, unique=True)  # 학번
    department = models.CharField(max_length=100)             # 학과
    major_choice = models.CharField(
        max_length=100,
        choices=[  # 복수/부/연계전공 드롭다운 옵션
            ('double', '복수전공'),
            ('minor', '부전공'),
            ('linked', '연계전공'),
            ('none', '해당 없음'),
        ],
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