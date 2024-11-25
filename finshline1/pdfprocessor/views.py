from django.shortcuts import render
from django.http import JsonResponse
from .forms import PDFUploadForm
from .utils import extract_text_from_pdf

# Create your views here.

def upload_pdf(request):
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_pdf = form.save()
            # PDF 텍스트 추출
            text = extract_text_from_pdf(uploaded_pdf.file)
            return JsonResponse({'text': text})
    else:
        form = PDFUploadForm()
    return render(request, 'upload_pdf.html', {'form': form})