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
# Create your views here.

# 회원가입 API
class SignUpAPIView(APIView):
    def get(self, request):
        return Response({"detail": "회원가입을 위해 POST 요청을 사용하세요."}, status=200)
    permission_classes = [AllowAny]

    def post(self, request):
        student_id = request.data.get('student_id')
        password = request.data.get('password')

        # 학생 인증: 웹 크롤링
        response = requests.post("https://portal.kwandong.ac.kr/login", data={
            'student_id': student_id,
            'password': password
        })

        if response.status_code == 200:
            # 크롤링된 정보 (예시 데이터 사용)
            username = "크롤링된 이름"
            department = "크롤링된 학과"
            request.data.update({'username': username, 'department': department})
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                token, _ = Token.objects.get_or_create(user=user)
                return Response({"token": token.key}, status=HTTP_200_OK)
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        return Response({"error": "학생 인증 실패"}, status=HTTP_400_BAD_REQUEST)

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

    def get(self, request):
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