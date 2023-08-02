from django.shortcuts import render, redirect
from django.db.models import Q, F
from django.utils import timezone
from artist.models import Artist
from support.models import Support, SupportForm, Bank, SupportFormStatus, Block
from alert.models import Alert
from userWorking.models import UserWorking
from hashlib import sha256

# 해시 생성
def calculate_hash(index, prev_hash, timestamp, inoutType, depositor, credit, creditTime):
    return sha256(f"{index}{prev_hash}{timestamp}{inoutType}{depositor}{credit}{creditTime}".encode()).hexdigest()

# 블록체인 생성
def create_new_bloack(support, supportForm, inoutType):
    prev_block = Block.objects.filter(support=support).order_by('timestamp').first()
    index = prev_block.index + 1
    timestamp = timezone.now()
    hash = calculate_hash(index, prev_block.hash, timestamp, '입금', supportForm.depositor, supportForm.credit,
                          supportForm.creditTime)
    return Block.objects.create(
        support=support,
        index=index,
        prev_hash=prev_block.hash,
        timestamp=timestamp,
        hash=hash,
        inoutType=inoutType,
        depositor=supportForm.depositor,
        credit=supportForm.credit,
        creditTime=supportForm.creditTime
    )

# 전체조회(진행중)
def support_list(request, pk):
    artist = Artist.objects.get(pk=pk)
    supports = Support.objects.filter(artist=artist, status='진행중')
    alert = Alert.objects.filter(user=request.user)
    return render(request, './support/support_list.html', {"supports":supports, "artist":artist, "alert":alert})

# 전체조회(완료)
def support_list_complete(request, pk):
    artist = Artist.objects.get(pk=pk)
    supports = Support.objects.filter(artist=artist, status='완료')
    alert = Alert.objects.filter(user=request.user)
    return render(request, './support/support_list.html', {"supports": supports, "artist": artist, "alert": alert})

# 내가 참여한 서포트(진행 중)
def my_support_list(request, pk):
    artist = Artist.objects.get(pk=pk)
    supports = Support.objects.filter(
        Q(artist=artist, user=request.user, status='진행중')| Q(artist=artist, form__user=request.user,
                                                               status='진행중')).distinct()
    alert = Alert.objects.filter(user=request.user)
    return render(request, './support/support_list_my.html', {"supports":supports, "artist":artist, "alert":alert})

# 내가 참여한 서포트(완료)
def my_support_list_complete(request, pk):
    artist = Artist.objects.get(pk=pk)
    supports = Support.objects.filter(
        Q(artist=artist, user=request.user, status='완료') | Q(artist=artist, form__user=request.user,
                                                              status='완료')).distinct()
    alert = Alert.objects.filter(user=request.user)
    return render(request, './support/support_list_my.html',
                  {"supports": supports, "artist": artist, "alert": alert})

# 상세조회(미완성)
def support_dtl(request, pk, spt_pk):
    artist=Artist.objects.get(pk=pk)
    support=Support.objects.get(pk=spt_pk)
    support_form=SupportForm.objects.filter(support=support)

    if request.method=='GET':
        return render(request, './support/support_dtl.html', {"support":support, "artist":artist, "support_form":support_form})
    # 모집종료
    # 대기중 서포트 폼 상태 변경


# 서포트 참여 폼 입력
def create_support_form(request, pk, spt_pk):
    artist = Artist.objects.get(pk=pk)
    user = request.user
    support = Support.objects.get(pk=spt_pk)
    alert = Alert.objects.filter(user=user)

    if request.method=='GET':
        return render(request, './support/support_form.html', {"support":support, "artist":artist, "alert": alert})

    # 제출 로직
    if request.method=='POST':
        depositor=request.POST.get('depositor')
        credit=request.POST.get('credit')
        creditTime=request.POST.get('creditTime')

        supportForm = SupportForm.objects.create(
            support=support,
            user=user,
            depositor=depositor,
            credit=credit,
            creditTime=creditTime,
        )
        #계좌 내역과 입력 폼 비교
        current_time = timezone.now()
        thirty_minutes_ago = current_time - timezone.timedelta(minutes=30)
        thirty_minutes_later = current_time + timezone.timedelta(minutes=30)
        try:
            bank = Bank.objects.get(
                support=support,
                depositor=depositor,
                credit=credit,
                creditTime__gte=thirty_minutes_ago,
                creditTime__lte=thirty_minutes_later
            )
            if bank:
                userWorking = UserWorking.objects.get(user=user, artist=artist)
                userWorking.supportGuest += 1
                supportForm.status = SupportFormStatus.auto_check.value
                support.balanceAmt += bank.credit
                userWorking.save()
                supportForm.save()
                support.save()
                # 블록 체인 생성
                create_new_bloack(support, supportForm, '입금')
                # 성공 알림 생성
                Alert.objects.create(
                    user=user,
                    message=F'{support.title}의 모금 내역이 자동 확인 되었습니다! 🎉',
                )

        except Bank.DoesNotExist:
            # 실패 알림 생성
            Alert.objects.create(
                user=user,
                message=F'{support.title}의 모금 내역이 확인되지 않았습니다. 입력 정보를 확인해 주세요.',
            )

        return redirect('support:support_dtl', pk=artist.pk, spt_pk=support.pk)

#서포트 게시글 생성
def create_support(request, pk):
    user=request.user
    artist=Artist.objects.get(pk=pk)
    alert = Alert.objects.filter(user=user)

    if request.method == 'GET':
        return render(request, './support/support_create.html', {"artist":artist, "alert":alert})

    if request.method == "POST":
        title = request.POST.get('title')
        fundraising = request.POST.get('fundraising')
        body = request.POST.get('body')
        image = request.FILES.get('image')
        bank = request.POST.get('bank')
        account = request.POST.get('account')
        deadline = request.POST.get('deadline')

        support = Support.objects.create(
            artist=artist,
            user=user,
            title=title,
            fundraising=fundraising,
            image=image,
            body=body,
            bank=bank,
            account=account,
            deadline=deadline
        )
        # 제네시스 블록 생성
        Block.objects.create(
            support=support,
            index=0,
            prev_hash="0",
            hash="0"
        )
        # 성공 알림 생성
        Alert.objects.create(
            user=user,
            message=F'<{support.title}> 서포트가 등록되었습니다!',
        )
        userWorking=UserWorking.objects.get(user=user, artist=artist)
        userWorking.supportHost += 1
        userWorking.save()
        return redirect('support:support_list', pk=artist.pk)

#서포트 게시글 수정
def update_support(request, pk, spt_pk):
    artist = Artist.objects.get(pk=pk)
    support = Support.objects.get(pk=spt_pk)
    alert = Alert.objects.filter(user=request.user)

    if not request.user == support.user:
        return redirect('support:support_dtl', pk=artist.pk, spt_pk=support.pk)

    if request.method == 'GET':
        return render(request, './support/support_update.html', {"support":support, "artist":artist, "alert":alert})

    if request.method == 'POST':
        title=request.POST.get('title')
        body=request.POST.get('body')
        fundraising=request.POST.get('fundraising')
        image=request.FILES.get('image')
        deadline=request.POST.get('deadline')

        if image is None:
            image = support.image

        if not deadline.strip():
            deadline = support.deadline

        support.title=title
        support.body=body
        support.fundraising=fundraising
        support.image=image
        support.deadline=deadline
        support.save()
        return redirect('support:support_dtl', pk=artist.pk, spt_pk=support.pk)