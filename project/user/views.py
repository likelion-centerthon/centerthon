from django.contrib.auth import login, authenticate
from django.utils import timezone
from django.shortcuts import render,redirect
from django.views.generic import View, CreateView, UpdateView, DeleteView

from .models import User
from artist.models import Artist
import requests

uri = "http://127.0.0.1:8000"

# 로그인 템플릿
def oauth_login(request):
    return render(request, './user/login.html', {"title":"Main"})

# 회원가입 상세정보 입력
def sign_up(request, pk):
    if not request.user.pk == pk:
        return redirect('user:login')
    if request.method=='GET':
        user = User.objects.get(pk=pk)
        return render(request, './user/signup.html', {"user":user})
    elif request.method=='POST':
        user = request.user
        user.age=request.POST.get('age')
        user.phoneNumber=request.POST.get('phoneNumber')
        user.subPhoneNumber=request.POST.get('subPhoneNumber')
        user.region=request.POST.get('region')
        user.save()

        return redirect('user:tutorial')

# 아티스트선택/튜토리얼 분기 페이지
def tutorial(request):
    return render(request, './user/tutorial.html')



# 인가 코드 요청
class Kakao(View):
    def get(self, request):
        kakao_api="https://kauth.kakao.com/oauth/authorize?response_type=code"
        redirect_uri=f"{uri}/oauth/callback"
        client_id="714db211a2aee35b2ed21cfed611dd34"
        return redirect(f"{kakao_api}&client_id={client_id}&redirect_uri={redirect_uri}")

# 토큰 발급 및 회원가입
class KakaoCallback(View):
    def get(self, request):
        data = {
            "grant_type":"authorization_code",
            "client_id":"714db211a2aee35b2ed21cfed611dd34",
            "redirection_uri":f"{uri}/users/oauth",
            "code":request.GET["code"]
        }
        kakao_token_api="https://kauth.kakao.com/oauth/token"
        access_token = requests.post(kakao_token_api, data=data).json().get("access_token")
        #카카오 사용자 정보 요청
        kakao_user_api="https://kapi.kakao.com/v2/user/me"
        user_info=requests.get(kakao_user_api, headers={"Authorization":f"Bearer ${access_token}"}).json()
        # print(user_info)
        if not User.objects.filter(kakaoId=user_info['id']).exists():
            if user_info['kakao_account']['gender']:
                user = User.objects.create(
                    kakaoId=user_info['id'],
                    userName=user_info['properties']['nickname'],
                    gender=user_info['kakao_account']['gender'],
                    last_login=timezone.now(),
                    password="1234",
                )
            else:
                user = User.objects.create(
                    kakaoId=user_info['id'],
                    userName=user_info['properties']['nickname'],
                    last_login=timezone.now(),
                    password="1234",
                )
            return redirect('user:signup', pk=user.pk)
        # 로그인
        user = User.objects.get(kakaoId=user_info['id'])
        login(request, user, 'user.auth.MyBackend')
        if user.artists.all().exists(): # 구독한 아티스트가 있다면 구독 아티스트로 이동
            return redirect('artist:subscribe_list', category='none')
        else: # 첫 사용자라면 아티스트 전체조회로 이동
            return redirect('user:signup', pk=user.pk)

# 튜토리얼 분기 페이지 1 (튜토리얼 진행하기 / 아티스트 선택하기)
def tutorial_next(request):
    return render(request, 'user/tutorial_next.html')

# 튜토리얼 분기 페이지 - 아티스트
def tutorial_artist_info(request):
    return render(request, 'tutorial_artist/tutorial_artist_info.html')

# 튜토리얼 분기 페이지 - 모임
def tutorial_meeting(request):
    return render(request, 'user/tutorial_meeting.html')

# 튜토리얼 분기 페이지 - 서포트
def tutorial_support(request):
    return render(request, 'user/tutorial_support.html')

# 전체 튜토리얼 진행
def tutorial_all(request):
    return render(request, 'user/tutorial_all.html')

# 구독한 아티스트 확인 튜토리얼
def tutorial_subscribe_artist(request):
    return render(request, 'tutorial_artist/tutorial_subscribe_artist.html')

# 추가 구독 튜토리얼
def tutorial_artist_list(request):
    return render(request, 'tutorial_artist/tutorial_artist_list.html')

#모임 리스트 튜토리얼
def tutorial_meeting_list(request):
    return render(request, 'tutorial_meeting/tutorial_meeting_list.html')

# 모임 참여 튜토리얼
def tutorial_meeting_manage(request):
    return render(request, 'tutorial_meeting/tutorial_meeting_manage.html')

# 모임 작성
def tutorial_meeting_start(request):
    return render(request, 'tutorial_meeting/tutorial_meeting_start.html')

#모임 관리 튜토리얼-작성
def tutorial_meeting_writed(request):
    return render(request, 'tutorial_meeting/tutorial_meeting_writed.html')

#모임 관리 튜토리얼-신청
def tutorial_meeting_apply(request):
    return render(request, 'tutorial_meeting/tutorial_meeting_apply.html')

#모임 관리 튜토리얼-보호자
def tutorial_meeting_pn(request):
    return render(request, 'tutorial_meeting/tutorial_meeting_pn.html')

# 서포트 참여 튜토리얼
def tutorial_support_manage_list(request):
    return render(request, 'tutorial_support/tutorial_support_manage_list.html')
def tutorial_support_manage_form(request):
    return render(request, 'tutorial_support/tutorial_support_manage_form.html')
def tutorial_support_manage_detail_1(request):
    return render(request, 'tutorial_support/tutorial_support_manage_detail_01.html')
def tutorial_support_manage_detail_2(request):
    return render(request, 'tutorial_support/tutorial_support_manage_detail_02.html')



# 서포트 작성 및 관리 튜토리얼
def tutorial_support_start(request):
    return render(request, 'tutorial_support/tutorial_support_start.html')