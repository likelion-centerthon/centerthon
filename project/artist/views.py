
from django.shortcuts import render, get_object_or_404, redirect

from artist.models import Artist

# 아티스트 조회
def artist_list(request):
    user = request.user

    if user.is_authenticated:
        if request.method == 'GET': # 아티스트 전체 조회
            artists = Artist.objects.all()

        if request.method == 'POST': # 구독한 아티스트 조회
            artists = user.artists.objects.all()

        return render(request, 'artist/artist_list.html', context={'artists': artists})

    return redirect('user:login')


# 아티스트 선택 후 아티스트 정보 페이지 이동
def select_artist(request, pk):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = request.user
            artist = get_object_or_404(Artist, pk=pk)
            user.artists.add(artist)
            return render(request, 'artist/artist_info.html', context={'artist':artist})

    return redirect('user:login')

