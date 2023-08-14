from django.shortcuts import render, redirect

from alert.models import Alert
from artist.models import Artist


# 알림 버튼 클릭 시 읽음 여부 true 변경
def check_alert(request, pk):
    user = request.user
    artist = Artist.objects.get(pk=pk)

    if not user.is_authenticated:
        redirect('user:login')

    if request.method == 'POST':

        alerts = Alert.objects.filter(user=user).order_by('-regTime')

        # 읽음 여부 필드 변경
        for alert in alerts:
            alert.is_read = True
            alert.save()

        return render(request, 'header.html', context={'alerts':alerts, 'artist':artist})

