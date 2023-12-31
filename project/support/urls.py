from django.urls import path
from support.views import support_list, create_support, support_list_complete, support_dtl, create_support_form, \
    my_support_list, my_support_list_complete, update_support, create_support_step_1, create_support_step_2, create_support_step_3

app_name = "support"

urlpatterns = [
    # 전체목록
    path('<int:pk>/posts/', support_list, name='support_list'),
    path('<int:pk>/posts/complete/', support_list_complete, name='support_list_complete'),
    path('<int:pk>/my/', my_support_list, name='my_support_list'),
    path('<int:pk>/my/complete/', my_support_list_complete, name='my_support_list_complete'),
    # 생성
    path('<int:pk>/new/', create_support, name='create_support'),
    path('<int:pk>/new/step_1/<int:spt_pk>/', create_support_step_1, name='create_support_step_1'),
    path('<int:pk>/new/step_2/<int:spt_pk>/', create_support_step_2, name='create_support_step_2'),
    path('<int:pk>/new/step_3/<int:spt_pk>/', create_support_step_3, name='create_support_step_3'),

    # 상세보기
    path('<int:pk>/post/<int:spt_pk>/', support_dtl, name='support_dtl'),
    # 수정
    path('<int:pk>/update/<int:spt_pk>/', update_support, name='update_support'),
    # 모금정보 작성
    path('<int:pk>/post/<int:spt_pk>/form/', create_support_form, name='create_support_form')
]