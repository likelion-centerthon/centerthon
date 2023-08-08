from django.urls import path

from alert.views import check_alert

app_name = 'alert'

urlpatterns = [
    path('<int:pk>/', check_alert, name='check_alert'),
]