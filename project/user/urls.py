from django.urls import path
from .views import oauth_login, Kakao, KakaoCallback, sign_up, tutorial, tutorial_next, tutorial_all, \
    tutorial_artist_info, tutorial_subscribe_artist, tutorial_artist_list, tutorial_meeting_start, \
    tutorial_meeting_manage, tutorial_support_start, tutorial_meeting, \
    tutorial_support, tutorial_support_join_list, tutorial_support_join_form, tutorial_support_join_detail_1, \
    tutorial_support_join_detail_2, tutorial_support_manage, tutorial_support_manage_detail_1, \
    tutorial_support_manage_detail_2

app_name = "user"

urlpatterns = [
    path("", oauth_login, name='login'),
    path("<int:pk>/", sign_up, name='signup'),
    path("oauth/", Kakao.as_view(), name='oauth'),
    path("oauth/callback/", KakaoCallback.as_view()),

    # 튜토리얼 분기
    path("tutorial/", tutorial, name='tutorial'),
    path('tutorial/next', tutorial_next, name='tutorial_next'),
    path('tutorial/all', tutorial_all, name='tutorial_all'),
    path('tutorial/meeting', tutorial_meeting, name='tutorial_meeting'),
    path('tutorial/support', tutorial_support, name='tutorial_support'),

    # 튜토리얼 아티스트
    path('tutorial/artist-info', tutorial_artist_info, name='tutorial_artist_info'),
    path('tutorial/subscribe-artist', tutorial_subscribe_artist, name='tutorial_subscribe_artist'),
    path('tutorial/artist-list', tutorial_artist_list, name='tutorial_artist_list'),

    # 튜토리얼 모임
    path('tutorial/meeting-manage', tutorial_meeting_manage, name='tutorial_meeting_manage'),
    path('tutorial/meeting-start', tutorial_meeting_start, name='tutorial_meeting_start'),

    # 튜토리얼 서포트
    # 서포트 참여
    path('tutorial/support-join', tutorial_support_join_list, name='tutorial_support_join'),
    path('tutorial/support-join-form', tutorial_support_join_form, name='tutorial_support_join_form'),
    path('tutorial/support-join-detail-1', tutorial_support_join_detail_1, name='tutorial_support_join_detail_1'),
    path('tutorial/support-join-detail-2', tutorial_support_join_detail_2, name='tutorial_support_join_detail_2'),
    # 서포트 생성
    path('tutorial/support-start', tutorial_support_start, name='tutorial_support_start'),
    # 서포트 관리
    path('tutorial/support-manage', tutorial_support_manage, name='tutorial_support_manage'),
    path('tutorial/support-manage-detail-1', tutorial_support_manage_detail_1, name='tutorial_support_manage_detail_1'),
    path('tutorial/support-manage-detail-2', tutorial_support_manage_detail_2, name='tutorial_support_manage_detail_2'),

]