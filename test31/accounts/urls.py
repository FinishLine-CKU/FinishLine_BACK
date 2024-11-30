from django.urls import path
from .views import SignUpAPIView, LoginAPIView, LogoutAPIView,PDFUploadAPIView

urlpatterns = [
    path('signup/', SignUpAPIView.as_view(), name='signup'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('upload-pdfs/', PDFUploadAPIView.as_view(), name='upload_pdfs'),
]
