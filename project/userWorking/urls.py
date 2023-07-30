from django.urls import path

from userWorking.views import show_userWorking

app_name = "userWorking"

urlpatterns = [
    path('<int:pk>/', show_userWorking, name='show_userWorking'),
]