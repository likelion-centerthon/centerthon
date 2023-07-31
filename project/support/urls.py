from django.urls import path
from support.views import support_list, create_support, support_list_complete, support_dtl, create_support_form

app_name = "support"

urlpatterns = [
    # 전체목록
    path('<int:pk>/posts/', support_list, name='support_list'),
    path('<int:pk>/posts/complete/', support_list_complete, name='support_list_complete'),
    # 생성
    path('<int:pk>/new/', create_support, name='create_support'),
    # 상세보기
    path('<int:pk>/post/<int:spt_pk>/', support_dtl, name='support_dtl'),
    # 수정
    # 삭제
    # 모금정보 작성
    path('<int:pk>/post/<int:spt_pk>/form/', create_support_form, name='create_support_form')
]