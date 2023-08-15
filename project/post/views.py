from django.utils import timezone

from alert.models import Alert
from django.shortcuts import render, redirect, get_object_or_404

from artist.models import Artist
from post.models import Post, Comment
from userWorking.models import UserWorking


# 게시글 전체 조회, 카테고리 분류
def post_list(request, artist_pk, category):
    user = request.user
    unread_alerts = Alert.objects.filter(user=user, is_read=False).order_by('-regTime')
    alerts = Alert.objects.filter(user=user)

    if not user.is_authenticated:
        return redirect('user:login')

    artist = Artist.objects.get(pk=artist_pk)
    posts = Post.objects.filter(category=category, artist=artist).order_by('-regTime')


    return render(request, 'post/post_list.html', context={'posts':posts, 'artist':artist, 'alerts':alerts, 'unread_alerts':unread_alerts,'category':category})


# 게시글 상세 조회
def post_detail(request, pk):
    user = request.user
    unread_alerts = Alert.objects.filter(user=user, is_read=False).order_by('-regTime')
    alerts = Alert.objects.filter(user=user)

    if not user.is_authenticated:
        return redirect('user:login')

    if request.method == 'GET':
        post = Post.objects.get(pk=pk)
        comments = Comment.objects.filter(post=post)

        return render(request, 'post/post_detail.html', context={'post':post, 'comments':comments, 'artist':post.artist, 'alerts':alerts, 'unread_alerts':unread_alerts})

# 게시글 생성
def create_post(request, artist_pk):
    user = request.user
    artist = Artist.objects.get(pk=artist_pk)
    unread_alerts = Alert.objects.filter(user=user, is_read=False).order_by('-regTime')
    alerts = Alert.objects.filter(user=user)

    if not user.is_authenticated:
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
        )

        # 게시글 작성 시 알림 생성
        Alert.objects.create(
            user=user,
            artist=artist,
            message=F'<{title}> 게시글이 등록되었습니다!',
            regTime=timezone.now()
        )

        # 이용행보 수정
        userWorking = UserWorking.objects.get(user=user, artist=artist)
        userWorking.postRecord += 1
        userWorking.save()

        return redirect('post:post_list', artist_pk=artist.pk, category=category)

    return render(request, 'post/create_post.html', context={'artist':artist, 'alerts':alerts, 'unread_alerts':unread_alerts})


# 게시글 수정
def edit_post(request, pk):
    user = request.user
    unread_alerts = Alert.objects.filter(user=user, is_read=False).order_by('-regTime')
    alerts = Alert.objects.filter(user=user)

    if not user.is_authenticated:
        return redirect('user:login')

    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":

        category = request.POST.get('category')
        title = request.POST.get('title')
        contents = request.POST.get('contents')
        image = request.FILES.get('image')

        if image is None:
            # 새로운 이미지가 제출되지 않은 경우 기존 이미지 유지
            image = post.image

        # 데이터 변경
        post.category = category
        post.title = title
        post.contents = contents
        post.image = image

        post.save()

        return redirect('post:post_list', artist_pk=post.artist.pk, category=category)

    else:
        return render(request, 'post/modify_post.html', context={'post': post, 'artist':post.artist, 'alerts':alerts, 'unread_alerts':unread_alerts})

# 게시글 삭제
def delete_post(request, pk):
    user = request.user

    if not user.is_authenticated:
        return redirect('user:login')

    if request.method == "GET":
        post = Post.objects.get(pk=pk)
        artist = post.artist
        post.delete()

        # 이용행보 수정
        userWorking = UserWorking.objects.get(user=user, artist=artist)
        userWorking.postRecord -= 1
        userWorking.save()

        return redirect('post:post_list', artist_pk=post.artist.pk, category=post.category)

    return render(request, 'post/failDelete.html')


# 댓글 생성
def create_comment(request, pk):
    user = request.user
    post = Post.objects.get(pk=pk)

    if not user.is_authenticated:
        return redirect('user:login')  # 로그인 페이지 이동

    if request.method == 'POST':
        contents = request.POST.get('contents')

        Comment.objects.create(
            post=post,
            author=user,
            contents=contents
        )

        # 댓글 작성 시 알림 생성
        Alert.objects.create(
            user=post.author,
            artist=post.artist,
            message=user.userName + '님이 <' + post.title + '> 게시글에 댓글을 남겼습니다.',
            regTime = timezone.now()
        )

        # 이용행보 수정
        userWorking = UserWorking.objects.get(user=user, artist=post.artist)
        userWorking.commentRecord += 1
        userWorking.save()

        return redirect('post:post_detail', pk=post.pk)

# 댓글 삭제
def delete_comment(request, pk):
    user = request.user

    if not user.is_authenticated:
        return redirect('user:login')

    if request.method == "GET":
        comment = Comment.objects.get(pk=pk)
        artist = comment.post.artist

        post = comment.post
        comment.delete()

        comments = Comment.objects.filter(post=comment.post)

        # 이용행보 수정
        userWorking = UserWorking.objects.get(user=user, artist=post.artist)
        userWorking.commentRecord -= 1
        userWorking.save()

        return render(request, 'post/post_detail.html', context={'post':comment.post, 'comments':comments, 'artist':artist})