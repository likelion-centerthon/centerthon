from django.shortcuts import render, redirect, get_object_or_404
from .models import Meeting, MeetingMember,MeetingState, MemberState
from artist.models import Artist
from django.db.models import Q


#모임 생성
def CreateMeeting(request, artist_id):
    artist =get_object_or_404(Artist, pk=artist_id)

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
        return redirect('createMeeting', artist_id=artist_id)

    return render(request, "html/meeting_create.html")

#모임 각각 상세조회
def MeetingDtl(request, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id)
    if meeting.writeUser == request.user:
        return render(request, "html/meeting_detail_admin.html", {'meeting': meeting})
    return render(request, "html/meeting_detail.html", {'meeting': meeting})

#모집 중인 모임 목록
def MeetingList(reqeust, artist_id):
    artists = Artist.objects.all()
    artist =get_object_or_404(Artist, pk=artist_id)
    meetings = artist.artist_meetings.all()
    meetings_recruiting = meetings.filter(meetingState=MeetingState.모집중.value)
    context = {
        'meetings_recruiting': meetings_recruiting,
        'artist_id': artist_id,
        'artist': artist,
        'artists' : artists,
    }
    return render(reqeust, "html/meeting_list.html", context)

#모집 완료된 모임 목록
def MeetingCloseList(reqeust, artist_id):
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
    }
    return render(reqeust, "html/meeting_completed_list.html", context)

#모임 상태 모집 완료로 바꾸기
def closeMeeting(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id)
    meeting.meetingState = MeetingState.모집완료.value
    meeting.save()
    return redirect('meeting_detail', meeting_id=meeting_id)

#모임 신청
def applyMeeting(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id)
    meetingMember=MeetingMember.objects.create(User=request.user, Meeting = meeting)
    meeting_members = meeting.members.all()
    print(meeting_members)
    meetingMember.save
    meeting.save
    context = {
        'meeting_id': meeting_id
    }
    return redirect('meeting_detail', meeting_id=meeting_id)

#수정 필요
def editMeeting(request, meeting_id):
    meeting = Meeting.objects.get(id=meeting_id)

    if request.method == 'POST':
        title = request.POST.get('title')
        body = request.POST.get('body')
        meetDate = request.POST.get('meetDate')
        location = request.POST.get('location')
        age = request.POST.get('age')
        peopleNm = request.POST.get('peopleNm')
        kakaoLink = request.POST.get('kakaoLink')
        meeting.title = title
        meeting.body = body
        meeting.meetDate = meetDate
        meeting.location = location
        meeting.age = age
        meeting.peopleNm = peopleNm
        meeting.kakaoLink = kakaoLink
        if 'image' in request.FILES:
            meeting.image = request.FILES['image']

        meeting.save()

        return redirect('meeting_detail', meeting_id=meeting_id)

    context = {'meeting': meeting}
    return render(request, "html/meeting_edit.html", context)

#내가 작성한 모임 리스

# 뷰함수
def writedMeetingList(request, artist_id):
    artists = Artist.objects.all()
    artist = get_object_or_404(Artist, pk=artist_id)
    search = request.GET.get('search')

    meetings = Meeting.objects.filter(writeUser=request.user, artist=artist)
    if search:
        meetings = meetings.filter(members__User__userName__icontains=search).distinct()

    return render(request, 'html/writed_meeting_list.html', {'meetings': meetings, 'artist_id': artist_id, 'artists': artists, 'artist': artist, 'search': search})


#모임 신청자 수락
def memberStateAccept(request, meetingMember_id, artist_id):
    member = MeetingMember.objects.get(id=meetingMember_id)
    member.memberState = MemberState.승인.value
    member.save()
    return redirect('writedMeetingList', artist_id = artist_id)

#모임 신청자 거부
def memberStateRefusal(request, meetingMember_id, artist_id):
    meetingMember = get_object_or_404(MeetingMember, id=meetingMember_id)
    meetingMember.memberState = "거부"
    meetingMember.save()
    return redirect('writedMeetingList', artist_id = artist_id)

#내가 신청한 모임 목록
def applyedMeetingList(request, artist_id):
    artists = Artist.objects.all()
    artist = get_object_or_404(Artist, pk=artist_id)
    meeting = Meeting.objects.filter(artist=artist)
    applyedMeetings = MeetingMember.objects.filter(User=request.user, Meeting__in=meeting)

    # URL에서 검색 쿼리 파라미터를 가져옵니다.
    search_query = request.GET.get('search')

    if search_query:
        # 검색 쿼리를 이용하여 모임을 필터링합니다.
        applyedMeetings = applyedMeetings.filter(Meeting__title__icontains=search_query)

    return render(request, 'html/applyed_meeting_list.html', {'applyedMeetings': applyedMeetings, 'artist_id': artist_id, 'artists': artists, 'artist': artist})


#신청자 보호자 번호 조회
def subPNList(request, artist_id):
    artists = Artist.objects.all()
    artist = get_object_or_404(Artist,pk=artist_id)
    search = request.GET.get('search')
    meetings = Meeting.objects.filter(writeUser=request.user, artist=artist)

    if search:
        meetings = meetings.filter(members__User__userName__icontains=search).distinct()

    return render(request, 'html/writed_meeting_PN.html', {'meetings': meetings, 'artist_id': artist_id,'artists' : artists,'artist' : artist, 'search': search})


