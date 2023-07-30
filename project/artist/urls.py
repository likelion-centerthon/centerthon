from django.urls import path

from artist.views import artist_list, select_artist, artist_sns, subscribe_list

app_name = "artist"

urlpatterns = [
    path('<str:category>/', artist_list, name='artist_list'), # 아티스트 조회
    path('<str:category>/subscribe/', subscribe_list, name='subscribe_list'), # 구독한 아티스트 조회
    path('<int:pk>/', select_artist, name='select_artist'),  # 아티스트 선택 후 아티스트 정보 페이지 이동
    path('<int:pk>/sns/', artist_sns, name='artist_sns'), # sns 페이지 이동
]