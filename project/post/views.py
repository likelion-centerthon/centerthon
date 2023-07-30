from datetime import timezone

from django.shortcuts import render, redirect, get_object_or_404

from artist.models import Artist
from post.models import Post


def post_list(request, category, artist_pk):
    user = request.user

    if not user.is_athenticated:
        return redirect('user:login')

    posts = Post.objects.filter(category=category )

    return render(request, 'post/post_list.html', context={'posts':posts})


def post_detail(request, pk):
    user = request.user

    if not user.is_athenticated:
        return redirect('user:login')

    if request.method == 'POST':
        post = Post.objects.get(pk=pk)
        return render(request, 'post/create_post', context='post')

def create_post(request, artist_pk):
    user = request.user
    artist = Artist.objects.get(pk=artist_pk)

    if not user.is_athenticated:
        return redirect('user:login')

    if request.method == "POST":
        title = request.POST.get('title')
        contents = request.POST.get('contents')
        category = request.POST.get('category')
        image = request.FILES.get('image')

        Post.objects.create(
            artist=artist,
            author=user,
            category=category,
            image=image,
            title=title,
            contents=contents,
            regTime=timezone.now()
        )

        return redirect('post:post_list', category=category)

def edit_post(request, pk):
    user = request.user

    if not user.is_athenticated:
        return redirect('user:login')

    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        category = request.POST.get('category')
        title = request.POST.get('title')
        contents = request.POST.get('contents')
        image = request.FILES.get('image')
        regTime = timezone.now()

        if image is None:
            # 새로운 이미지가 제출되지 않은 경우 기존 이미지 유지
            image = post.image

        # 데이터 변경
        post.category = category
        post.title = title
        post.contents = contents
        post.image = image
        post.regTime = regTime

        post.save()

        return redirect('post:post_list', category=category)

    return render(request, 'post/create_post.html', context={'post': post})


def delete_post(request, pk):
    user = request.user

    if not user.is_athenticated:
        return redirect('user:login')  # 로그인 페이지 이동

    if request.method == "GET":
        post = Post.objects.get(pk=pk)
        post.delete()
        return redirect('product:product_list', category=post.category)

    return render(request, 'post/failDelete.html')
