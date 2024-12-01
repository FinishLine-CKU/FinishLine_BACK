from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.hashers import make_password
from .models import UploadedPDF

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'student_id', 'department', 'major_choice', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # 비밀번호 암호화
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

class PDFUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedPDF
        fields = ['id', 'file', 'extracted_text', 'uploaded_at']