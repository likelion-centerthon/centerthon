from django.urls import path

from alert.views import show_alert

app_name = 'alert'

urlpatterns = [
    path('', show_alert, name='show_alert'),
]