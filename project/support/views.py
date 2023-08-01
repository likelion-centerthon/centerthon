from django.shortcuts import render, redirect
from django.db.models import Q
from artist.models import Artist
from support.models import Support, SupportForm


#전체조회(진행중)
def support_list(request, pk):
    artist = Artist.objects.get(pk=pk)
    supports = Support.objects.filter(artist=artist, status='진행중')
    #계좌의 총 잔액도 불러와야 함
    return render(request, './support/support_list.html', {"supports":supports, "artist":artist})

#전체조회(완료)
def support_list_complete(request, pk):
    artist = Artist.objects.get(pk=pk)
    supports = Support.objects.filter(artist=artist, status='완료')
    #계좌의 총 잔액도 불러와야 함
    return render(request, './support/support_list.html', {"supports":supports, "artist":artist})

#내가 참여한 서포트(진행 중)
def my_support_list(request, pk):
    artist = Artist.objects.get(pk=pk)
    supports = Support.objects.filter(
        Q(artist=artist, user=request.user, status='진행중')| Q(artist=artist, form__user=request.user,
                                                               status='진행중')).distinct()
    return render(request, './support/support_list_my.html', {"supports":supports, "artist":artist})

#내가 참여한 서포트(완료)
def my_support_list_complete(request, pk):
    artist = Artist.objects.get(pk=pk)
    supports = Support.objects.filter(
        Q(artist=artist, user=request.user, status='완료') | Q(artist=artist, form__user=request.user,
                                                              status='완료')).distinct()
    return render(request, './support/support_list_my.html', {"supports": supports, "artist": artist})

#상세조회
def support_dtl(request, pk, spt_pk):
    artist=Artist.objects.get(pk=pk)
    support=Support.objects.get(pk=spt_pk)
    support_form=SupportForm.objects.filter(support=support)
    return render(request, './support/support_dtl.html', {"support":support, "artist":artist, "support_form":support_form})

#서포트 참여 폼 입력(미완성)
def create_support_form(request, pk, spt_pk):
    artist = Artist.objects.get(pk=pk)
    user = request.user
    support = Support.objects.get(pk=spt_pk)

    if request.method=='GET':
        return render(request, './support/support_form.html', {"support":support, "artist":artist})

    if request.method=='POST':
        depositor=request.POST.get('depositor')
        credit=request.POST.get('credit')
        creditTime=request.POST.get('creditTime')

        SupportForm.objects.create(
            support=support,
            user=user,
            depositor=depositor,
            credit=credit,
            creditTime=creditTime,
        )
        #입금정보 작성 직후 계좌 확인하는 로직 필요함
        return redirect('support:support_dtl', pk=artist.pk, spt_pk=support.pk)

#서포트 게시글 생성(미완성)
def create_support(request, pk):
    user=request.user
    artist=Artist.objects.get(pk=pk)

    if request.method == 'GET':
        return render(request, './support/support_create.html', {"artist":artist})

    if request.method == "POST":
        title = request.POST.get('title')
        fundraising = request.POST.get('fundraising')
        body = request.POST.get('body')
        image = request.FILES.get('image')
        bank = request.POST.get('bank')
        account = request.POST.get('account')
        deadline = request.POST.get('deadline')

        Support.objects.create(
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
        return redirect('support:support_list', pk=artist.pk)