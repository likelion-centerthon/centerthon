from django.urls import path, include

from artist.views import artist_list, select_artist

app_name = "artist"

urlpatterns = [
    path('', artist_list, name='artist_list'), # 아티스트 전체 조회
    path('<int:pk>/', select_artist, name='select_artist'), # 아티스트 선택 후 아티스트 정보 페이지 이동
]