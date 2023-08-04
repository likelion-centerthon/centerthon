from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect

from alert.models import Alert
from artist.models import Artist
from userWorking.models import UserWorking


# 아티스트 조회
def artist_list(request, category):
    user = request.user

    if user.is_authenticated:
        if request.method == 'GET': # 로그인 시 get 요청
            artists = Artist.objects.all()

        if request.method == 'POST': # 다른 아티스트 보러가기 시 post 요청
            if category == 'none':
                artists = Artist.objects.all()
            else: # 필터링
                artists = Artist.objects.filter(category=category)

        return render(request, 'artist/artist_list.html', context={'artists': artists})

    return redirect('user:login')

# 구독한 아티스트 조회
def subscribe_list(request, category):
    user = request.user

    if user.is_authenticated:
        if request.method == 'GET': # 로그인 시 get 요청
            artists = user.artists.all()

        if request.method == 'POST': # 필터링 시 post 요청
            artists = user.artists.all().filter(category=category)

        return render(request, 'artist/subscribe_list.html', context={'artists': artists})

    return redirect('user:login')



# 아티스트 선택 후 아티스트 정보 페이지 이동, 해당 아티스트 userWorking 생성
def select_artist(request, pk):
    if request.user.is_authenticated:
        user = request.user
        artist = get_object_or_404(Artist, pk=pk)
        alerts = Alert.objects.filter(user=user)

        # 유저 아티스트 필드에 추가
        user.artists.add(artist)

        # userWorking 생성

        if not UserWorking.objects.filter(user=user, artist=artist).exists():
            UserWorking.objects.create(
                user=user,
                artist=artist,
                startDay=timezone.now().date()
            )

        return render(request, 'artist/artist_info.html', context={'artist':artist, 'alerts':alerts})

    return redirect('user:login')

# sns 페이지 이동
def artist_sns(request, pk):
    user=request.user
    artist = get_object_or_404(Artist, pk=pk)
    alerts = Alert.objects.filter(user=user)

    if request.method == 'POST':
        return render(request, 'artist/artist_sns.html', context={'artist':artist, 'alerts':alerts})