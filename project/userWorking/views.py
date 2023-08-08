from django.shortcuts import render, redirect
from django.utils import timezone
from alert.models import Alert
from artist.models import Artist
from userWorking.models import UserWorking
from meeting.models import MeetingMember


def show_userWorking(request, pk):
    user = request.user
    artist = Artist.objects.get(pk=pk)
    alerts = Alert.objects.filter(user=user)

    if user.is_authenticated:
        if request.method == 'POST':
            userWorking = UserWorking.objects.get(user=user, artist=artist)

            currentDay = timezone.now().date()
            likeDays = currentDay - userWorking.startDay
            userWorking.likeDays = likeDays.days  # 올바른 방법: likeDays.days
            userWorking.save()

            return render(request, 'userWorking/userWorking.html', context={'userWorking':userWorking, 'artist':artist, 'alerts':alerts})

    return redirect('user:login')

def show_userWorking_guest(request, pk, meetingMember_id):
    member = MeetingMember.objects.get(id=meetingMember_id)
    user = member.User
    artist = Artist.objects.get(pk=pk)
    alerts = Alert.objects.filter(user=user)

    if user.is_authenticated:
        if request.method == 'POST':
            userWorking = UserWorking.objects.get(user=user, artist=artist)

            currentDay = timezone.now().date()
            likeDays = currentDay - userWorking.startDay
            userWorking.likeDays = likeDays.days  # 올바른 방법: likeDays.days
            userWorking.save()

            return render(request, 'userWorking/userWorking.html', context={'userWorking':userWorking, 'artist':artist, 'alerts':alerts})

    return redirect('user:login')