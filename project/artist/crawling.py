import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from .models import Music
def collect_and_save_data():
    URL = 'https://music.bugs.co.kr/search/integrated?q=%EC%9E%84%EC%98%81%EC%9B%85'
    request = requests.get(URL)
    html = request.text
    soup = BeautifulSoup(html, 'html.parser')

    titles = soup.select('p.title')
    artists = soup.select('p.artist')

    for i in range(len(titles)):
        title = titles[i].text.strip().split('\n')[0]
        artist = artists[i].text.strip().split('\n')[0]

        music = Music(title=title, artist=artist)
        music.save()
        print(music)
def music_chart(request):
    if not Music.objects.exists():
        collect_and_save_data()
    music_data = Music.objects.all()
    return render(request, 'artist/chart.html', {'music_data': music_data})

