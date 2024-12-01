import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser
from .serializers import UserSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from .models import UploadedPDF
from .serializers import PDFUploadSerializer
from .utils import extract_text_from_pdf
from .cku_login_macro import cku_login  # cku_login을 임포트합니다.
import json
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.middleware.csrf import get_token

# Create your views here.

# 회원가입 API
def student_authentication(request):
    if request.method == 'POST':
        # JSON 형식으로 데이터를 받음
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        if username and password:
            # cku_login 함수 호출하여 값 받기
            try:
                CrawlUserID, CrawlUserName, CrawlUserMajor = cku_login(username, password)
                
                # 받은 데이터를 JsonResponse로 반환
                return JsonResponse({
                    '학번': CrawlUserID,
                    '이름': CrawlUserName,
                    '전공': CrawlUserMajor
                })
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
        else:
            return JsonResponse({'error': '아이디와 비밀번호를 입력해주세요.'}, status=400)

    return JsonResponse({'error': '잘못된 요청입니다.'}, status=400)


class SignUpAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            # JSON 데이터 받기
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            crawl_user_id = data.get('학번')
            crawl_user_name = data.get('이름')
            crawl_user_major = data.get('전공')

            if not username or not password or not crawl_user_id or not crawl_user_name or not crawl_user_major:
                return Response({'error': '필수 정보를 모두 입력해주세요.'}, status=HTTP_400_BAD_REQUEST)

            # 시리얼라이저로 유저 생성
            data.update({
                'username': crawl_user_name,  # 크롤링된 이름
                'department': crawl_user_major,  # 크롤링된 학과
                'student_id': crawl_user_id  # 크롤링된 학번
            })
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                user = serializer.save()
                token, _ = Token.objects.get_or_create(user=user)
                return Response({"token": token.key}, status=HTTP_200_OK)

            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        except json.JSONDecodeError:
            return Response({'error': '유효하지 않은 JSON 데이터입니다.'}, status=HTTP_400_BAD_REQUEST)


# 로그인 API
class LoginAPIView(APIView):
    def get(self, request):
        return Response({"detail": "로그인을 위해 POST 요청을 사용하세요."})
    permission_classes = [AllowAny]

    def post(self, request):
        student_id = request.data.get('student_id')
        password = request.data.get('password')
        user = authenticate(username=student_id, password=password)
        if user:
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=HTTP_400_BAD_REQUEST)

# 로그아웃 API
class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "Successfully logged out"}, status=HTTP_200_OK)
    

# pdf업로드 API
class PDFUploadAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        files = request.FILES.getlist('file')  # 여러 파일 업로드 처리
        if len(files) > 25:
            return Response({"error": "최대 25개의 파일만 업로드 가능합니다."}, status=HTTP_400_BAD_REQUEST)
        
        uploaded_pdfs = []
        for file in files:
            try:
                extracted_text = extract_text_from_pdf(file)
                pdf_instance = UploadedPDF.objects.create(
                    user=request.user,
                    file=file,
                    extracted_text=extracted_text
                )
                uploaded_pdfs.append(pdf_instance)
            except Exception as e:
                return Response({"error": f"파일 처리 중 오류 발생: {str(e)}"}, status=HTTP_400_BAD_REQUEST)

        serializer = PDFUploadSerializer(uploaded_pdfs, many=True)
        return Response(serializer.data, status=HTTP_200_OK)