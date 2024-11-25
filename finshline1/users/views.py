from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import signupationForm,LoginForm
from users.models import User

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['student_id']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "로그인 성공!")
                return redirect('/')  # 로그인 후 이동할 페이지
            else:
                messages.error(request, "아이디 또는 비밀번호가 올바르지 않습니다.")
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


def signup_step1_view(request):

    #Step 1: 이용약관 및 학생 인증
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        password = request.POST.get('password')
        agree_terms = request.POST.get('agree_terms')

        # 이용약관 동의 체크 확인
        if not agree_terms:
            messages.error(request, "이용약관에 동의해야 합니다.")
            return render(request, 'users/signup_step1.html')

        # 학생 인증
        student_data = fake_student_auth(student_id, password)
        if student_data:
            # 세션에 인증된 정보 저장
            request.session['student_data'] = student_data
            return redirect('signup_step2')  # 다음 단계로 이동
        else:
            messages.error(request, "학생 인증에 실패했습니다. 포털 정보를 확인하세요.")
    return render(request, 'users/signup_step1.html')


def signup_step2_view(request):
    
    student_data = request.session.get('student_data')
    if not student_data:
        return redirect('signup_step1')  # 인증 없이 접근 시 첫 단계로 리다이렉트

    if request.method == 'POST':
        form = signupationForm(request.POST)
        
        if form.is_valid():
            # student_id가 이미 존재하는지 확인
            if User.objects.filter(student_id=student_data['student_id']).exists():
                messages.error(request, "이 학생 ID는 이미 등록되어 있습니다.")
                return render(request, 'users/signup_step2.html', {'form': form})

            user = form.save(commit=False)
            user.student_id = student_data['student_id']
            user.real_name = student_data['real_name']
            user.department = student_data['department']
            user.save()
            login(request,user)  # 로그인 후 이동
            messages.success(request, "회원가입이 완료되었습니다.")
            return redirect('users/login')  # 로그인 페이지로 이동
        else:
            print(form.errors)
    else:
        form = signupationForm(initial={
            'student_id': student_data['student_id'],
            'real_name': student_data['real_name'],
            'department': student_data['department'],
        })

    return render(request, 'users/signup_step2.html', {'form': form})
    

def fake_student_auth(student_id,password):

    #학생인증 Test
    if student_id == "202400020" and password == "password123":
        return {
            'student_id': '202400020',
            'real_name': '김수진',
            'department': '국어교육과'
        }
    return None


def logout_view(request):
    logout(request)
    messages.success(request, "로그아웃되었습니다.")
    return redirect('login')  # 로그아웃 후 로그인 페이지로 이동
