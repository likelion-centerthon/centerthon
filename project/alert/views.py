from django.shortcuts import render, redirect

from alert.models import Alert


def show_alert(request):
    user = request.user

    if not user.is_authenticated:
        redirect('user:login')

    if request.method == 'POST':
        alerts = Alert.objects.filter(user=user)
        return render(request, 'alert/show_alert.html', context={'alerts':alerts})
