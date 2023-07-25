from django.urls import path
from .views import oauth_login, Kakao, KakaoCallback, sign_up, select_artist

app_name = "user"

urlpatterns = [
    path("", oauth_login, name='login'),
    path("<int:pk>/", sign_up, name='signup'),
    path("oauth/", Kakao.as_view(), name='oauth'),
    path("oauth/callback/", KakaoCallback.as_view()),
    path("artist/", select_artist, name='artists'),
]