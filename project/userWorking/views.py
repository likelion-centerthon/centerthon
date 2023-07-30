from django.shortcuts import render, redirect

from artist.models import Artist
from userWorking.models import UserWorking


def show_userWorking(request, pk):
    user = request.user
    artist = Artist.objects.get(pk=pk)

    if user.is_athenticated():
        if request.method == 'POST':
            userWorking = UserWorking.objects.get(user=user, artist=artist)
            return render(request, 'userWorking:userWorking.html', context={'userWorking':userWorking})

    return redirect('user:login')