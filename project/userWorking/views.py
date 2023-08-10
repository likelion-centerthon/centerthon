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
            userWorkings = UserWorking.objects.filter(artist=artist)

            max_sum = 0
            user_sum = 0
            user_score = 0

            # 이용 행보 최대값 구하기
            for userWorking in userWorkings:
                current_sum = (
                    userWorking.likeDays
                    + userWorking.postRecord
                    + userWorking.commentRecord
                    + userWorking.meetingHost
                    + userWorking.meetingGuest
                    + userWorking.supportHost * 2
                    + userWorking.supportGuest * 2)

                if current_sum > max_sum:
                    max_sum = current_sum

                if userWorking.user == user:
                    user_sum = current_sum

            # 점수 계산
            if max_sum == user_sum:
                user_score = 100
            else:
                user_score = round((user_sum / max_sum) * 100)

            request_userWorking = UserWorking.objects.get(user=user, artist=artist)

            currentDay = timezone.now().date()
            likeDays = currentDay - request_userWorking.startDay
            request_userWorking.likeDays = likeDays.days
            request_userWorking.score = user_score

            request_userWorking.save()

            return render(request, 'userWorking/userWorking.html', context={'userWorking':request_userWorking, 'artist':artist, 'alerts':alerts})

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