from django.urls import path

from userWorking.views import show_userWorking,show_userWorking_guest

app_name = "userWorking"

urlpatterns = [
    path('<int:pk>/', show_userWorking, name='show_userWorking'),
    path('<int:pk>/<int:meetingMember_id>/', show_userWorking_guest, name='show_userWorking_guest'),

]