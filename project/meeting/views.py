from django.shortcuts import render, redirect, get_object_or_404
from .models import Meeting, MeetingMember, MeetingState, MemberState
from artist.models import Artist
from .forms import MeetingEditForm
from alert.models import Alert
from userWorking.models import UserWorking


#모임 생성
def CreateMeeting(request, artist_id):
    artist =get_object_or_404(Artist, pk=artist_id)
    user = request.user
    alerts = Alert.objects.filter(user=user)

    if request.method == 'POST' :
        meeting = Meeting()
        meeting.title = request.POST['title']
        meeting.body = request.POST['body']
        meeting.meetDate = request.POST['meetDate']
        meeting.location = request.POST['location']
        meeting.age = request.POST['age']
        meeting.peopleNm = request.POST['peopleNm']
        meeting.kakaoLink = request.POST['kakaoLink']
        meeting.image = request.FILES['image']
        meeting.writeUser = request.user
        meeting.artist = artist
        meeting.save()
        userWorking=UserWorking.objects.get(user=user, artist=artist)
        userWorking.meetingHost += 1
        userWorking.save()
        Alert.objects.create(user=user, artist=artist,
                             message=F'<{meeting.title}> 모임이 등록되었습니다!')
        return redirect('meeting:MeetingList', artist_id=artist_id)

    return render(request, "html/meeting_create.html", {'artist': artist, 'alerts': alerts})

#모임 각각 상세조회
def MeetingDtl(request, artist_id, meeting_id):
    artist =get_object_or_404(Artist, pk=artist_id)
    user = request.user
    alerts = Alert.objects.filter(user=user)
    meeting = get_object_or_404(Meeting, pk=meeting_id)
    # if meeting.writeUser == request.user:
    #     return render(request, "html/meeting_detail_admin.html", {'meeting': meeting, 'alerts':alerts, 'artist': artist})
    return render(request, "html/meeting_detail.html", {'meeting': meeting, 'alerts': alerts, 'artist': artist})

#모집 중인 모임 목록
def MeetingList(reqeust, artist_id):
    user = reqeust.user
    artists = user.artists.all()
    artist =get_object_or_404(Artist, pk=artist_id)
    meetings = artist.artist_meetings.all()
    meetings_recruiting = meetings.filter(meetingState=MeetingState.모집중.value)
    alerts = Alert.objects.filter(user=user)

    context = {
        'meetings_recruiting': meetings_recruiting,
        'artist_id': artist_id,
        'artist': artist,
        'artists' : artists,
        'alerts' : alerts
    }
    return render(reqeust, "html/meeting_list.html", context)

#모집 완료된 모임 목록
def MeetingCloseList(reqeust, artist_id):
    user = reqeust.user
    alerts = Alert.objects.filter(user=user)
    artists = Artist.objects.all()
    artist =get_object_or_404(Artist, pk=artist_id)
    meetings = artist.artist_meetings.all()
    meetings_completed = meetings.filter(meetingState=MeetingState.모집완료.value)
    meetings_recruiting = meetings.filter(meetingState=MeetingState.모집중.value)

    context = {
        'meetings_recruiting': meetings_recruiting,
        'meetings_completed': meetings_completed,
        'artist_id': artist_id,
        'artist': artist,
        'artists' : artists,
        'alerts' : alerts,
    }
    return render(reqeust, "html/meeting_completed_list.html", context)

#모임 상태 모집 완료로 바꾸기
def closeMeeting(request, meeting_id, artist_id):
    user = request.user
    alerts = Alert.objects.filter(user=user)
    artist = get_object_or_404(Artist, pk=artist_id)
    meeting = get_object_or_404(Meeting, id=meeting_id)
    meeting.meetingState = MeetingState.모집완료.value
    meeting.save()
    return redirect('meeting:meeting_detail', meeting_id=meeting_id, artist_id=artist_id)

#모임 신청
def applyMeeting(request, meeting_id, artist_id):
    user = request.user
    alerts = Alert.objects.filter(user=user)
    artist = get_object_or_404(Artist, pk=artist_id)
    meeting = get_object_or_404(Meeting, id=meeting_id)
    meetingMember=MeetingMember.objects.create(User=user, Meeting = meeting)
    meeting_members = meeting.members.all()
    meetingMember.save()
    meeting.save()
    Alert.objects.create(user=user, artist=artist,
                         message=F'<{meeting.title}> 모임을 신청했습니다!')
    context = {
        'meeting_id': meeting_id,
        'alerts' : alerts,
        'artist' : artist
    }
    return redirect('meeting:meeting_detail', meeting_id=meeting_id, artist_id=artist_id)

#수정 기능
def editMeeting(request,artist_id, meeting_id):
    user = request.user
    alerts = Alert.objects.filter(user=user)
    meeting = get_object_or_404(Meeting, id=meeting_id)
    artist = get_object_or_404(Artist, pk=artist_id)

    if request.method == 'POST':
        form = MeetingEditForm(request.POST, request.FILES, instance=meeting)
        if form.is_valid():
            form.save()
            return redirect('meeting:meeting_detail', meeting_id=meeting_id, artist_id=artist_id)
    else:
        form = MeetingEditForm(instance=meeting)

    context = {'form': form, 'meeting': meeting, 'alerts': alerts, 'artist': artist}
    return render(request, "html/meeting_edit.html", context)

#내가 작성한 모임 리스트
def writedMeetingList(request, artist_id):
    user = request.user
    alerts = Alert.objects.filter(user=user)
    artists = Artist.objects.all()
    artist = get_object_or_404(Artist, pk=artist_id)
    search = request.GET.get('search')

    meetings = Meeting.objects.filter(writeUser=user, artist=artist)
    if search:
        meetings = meetings.filter(members__User__userName__icontains=search).distinct()

    return render(request, 'html/writed_meeting_list.html', {'meetings': meetings, 'artist_id': artist_id, 'artists': artists, 'artist': artist, 'search': search, 'alerts':alerts})


#모임 신청자 수락
def memberStateAccept(request, meetingMember_id, artist_id):
    artist = get_object_or_404(Artist, pk=artist_id)
    member = MeetingMember.objects.get(id=meetingMember_id)
    member.memberState = MemberState.승인.value
    member.save()
    userWorking = UserWorking.objects.get(user=member.User, artist=artist)
    userWorking.meetingGuest += 1
    userWorking.save()
    Alert.objects.create(user=member.User, artist=artist,
                         message=F'<{member.Meeting.title}> 모임의 신청이 수락되었습니다!',
                        openChatURL=F'<{member.Meeting.kakaoLink}> 오픈채팅 링크에 접속하세요!')
    return redirect('meeting:writedMeetingList', artist_id = artist_id)

#모임 신청자 거부
def memberStateRefusal(request, meetingMember_id, artist_id):
    artist = get_object_or_404(Artist, pk=artist_id)
    meetingMember = get_object_or_404(MeetingMember, id=meetingMember_id)
    meetingMember.memberState = "거부"
    meetingMember.save()
    Alert.objects.create(user=meetingMember.User, artist=artist,
                         message=F'<{meetingMember.Meeting.title}> 모임의 신청이 거절되었습니다!')
    return redirect('meeting:writedMeetingList', artist_id = artist_id)

#내가 신청한 모임 목록
def applyedMeetingList(request, artist_id):
    user = request.user
    alerts = Alert.objects.filter(user=user)
    artists = Artist.objects.all()
    artist = get_object_or_404(Artist, pk=artist_id)
    meeting = Meeting.objects.filter(artist=artist)
    applyedMeetings = MeetingMember.objects.filter(User=request.user, Meeting__in=meeting)

    # URL에서 검색 쿼리 파라미터를 가져옵니다.
    search_query = request.GET.get('search')

    if search_query:
        # 검색 쿼리를 이용하여 모임을 필터링합니다.
        applyedMeetings = applyedMeetings.filter(Meeting__title__icontains=search_query)

    return render(request, 'html/applyed_meeting_list.html', {'applyedMeetings': applyedMeetings, 'artist_id': artist_id, 'artists': artists, 'artist': artist, 'alerts': alerts,})


#신청자 보호자 번호 조회
def subPNList(request, artist_id):
    user = request.user
    alerts = Alert.objects.filter(user=user)
    artists = Artist.objects.all()
    artist = get_object_or_404(Artist,pk=artist_id)
    search = request.GET.get('search')
    meetings = Meeting.objects.filter(writeUser=request.user, artist=artist)

    if search:
        meetings = meetings.filter(members__User__userName__icontains=search).distinct()

    return render(request, 'html/writed_meeting_PN.html', {'meetings': meetings, 'artist_id': artist_id,'artists' : artists,'artist' : artist, 'search': search, 'alerts':alerts,})

