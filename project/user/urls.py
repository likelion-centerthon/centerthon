from django.urls import path
from . import views
app_name = "user"

urlpatterns = [
    path("", views.oauth_login, name='login'),
    path("<int:pk>/", views.sign_up, name='signup'),
    path("oauth/", views.Kakao.as_view(), name='oauth'),
    path("oauth/callback/", views.KakaoCallback.as_view()),

    # 튜토리얼 분기
    path("tutorial/", views.tutorial, name='tutorial'),
    path('tutorial/next', views.tutorial_next, name='tutorial_next'),
    path('tutorial/all', views.tutorial_all, name='tutorial_all'),
    path('tutorial/meeting', views.tutorial_meeting, name='tutorial_meeting'),
    path('tutorial/support', views.tutorial_support, name='tutorial_support'),

    # 튜토리얼 아티스트
    path('tutorial/artist-first', views.tutorial_artist_first, name='tutorial_artist_first'),
    path('tutorial/artist-info', views.tutorial_artist_info, name='tutorial_artist_info'),
    path('tutorial/subscribe-list', views.tutorial_subscribe_artist, name='tutorial_subscribe_artist'),
    path('tutorial/artist-list', views.tutorial_artist_list, name='tutorial_artist_list'),

    # 튜토리얼 모임
    path('tutorial/meeting-first', views.tutorial_meeting_first, name='tutorial_meeting_first'),
    path('tutorial/meeting-manage', views.tutorial_meeting_manage, name='tutorial_meeting_manage'),
    path('tutorial/meeting-start',views.tutorial_meeting_start, name='tutorial_meeting_start'),
    path('tutorial/meeting-wirte', views.tutorial_meeting_writed, name='tutorial_meeting_writed'),
    path('tutorial/meeting-apply', views.tutorial_meeting_apply, name='tutorial_meeting_apply'),
    path('tutorial/meeting-pn', views.tutorial_meeting_pn, name='tutorial_meeting_pn'),
    path('tutorial/meeting-list', views.tutorial_meeting_list, name='tutorial_meeting_list'),
    path('tutorial/meeting-list-2',views.tutorial_meeting_list2,name='tutorial_meeting_list2'),

    # 튜토리얼 서포트
path('tutorial/support-first', views.tutorial_support_first, name='tutorial_support_first'),
    # path('tutorial/support-manage', views.tutorial_support_manage_list, name='tutorial_support_manage'),
    # path('tutorial/support-manage-form', views.tutorial_support_manage_form, name='tutorial_support_manage_form'),
    # 서포트 참여
    path('tutorial/support-join', views.tutorial_support_join_list, name='tutorial_support_join'),
    path('tutorial/support-join-form', views.tutorial_support_join_form, name='tutorial_support_join_form'),
    path('tutorial/support-join-detail-1', views.tutorial_support_join_detail_1, name='tutorial_support_join_detail_1'),
    path('tutorial/support-join-detail-2', views.tutorial_support_join_detail_2, name='tutorial_support_join_detail_2'),
    # 서포트 생성
    path('tutorial/support-start', views.tutorial_support_start, name='tutorial_support_start'),
    path('tutorial/support-start-form', views.tutorial_support_start_form, name='tutorial_support_start_form'),
    path('tutorial/support-start-step-1', views.tutorial_support_start_step_1, name='tutorial_support_start_step_1'),
    path('tutorial/support-start-step-2', views.tutorial_support_start_step_2, name='tutorial_support_start_step_2'),
    path('tutorial/support-start-step-3', views.tutorial_support_start_step_3, name='tutorial_support_start_step_3'),
    path('tutorial/support-start-step-4', views.tutorial_support_start_step_4, name='tutorial_support_start_step_4'),
    # 서포트 관리
    path('tutorial/support-manage', views.tutorial_support_manage, name='tutorial_support_manage'),
    path('tutorial/support-manage-detail-1', views.tutorial_support_manage_detail_1, name='tutorial_support_manage_detail_1'),
    path('tutorial/support-manage-detail-2', views.tutorial_support_manage_detail_2, name='tutorial_support_manage_detail_2'),
    path('tutorial/support-start', views.tutorial_support_start, name='tutorial_support_start'),

    ]