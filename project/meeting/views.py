from django.shortcuts import render, redirect, get_object_or_404
from .models import Meeting, MeetingMember,MeetingState
from artist.models import Artist


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

def MeetingDtl(request, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id)
    if meeting.writeUser == request.user:
        return render(request, "html/meeting_detail_admin.html", {'meeting': meeting})
    return render(request, "html/meeting_detail.html", {'meeting': meeting})

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

def MeetingCloseList(reqeust, artist_id):
    artist =get_object_or_404(Artist, pk=artist_id)
    meetings = artist.artist_meetings.all()
    meetings_completed = meetings.filter(meetingState=MeetingState.모집완료.value)
    meetings_recruiting = meetings.filter(meetingState=MeetingState.모집중.value)

    context = {
        'meetings_recruiting': meetings_recruiting,
        'meetings_completed': meetings_completed,
        'artist_id': artist_id,
        'artist': artist,
    }
    return render(reqeust, "html/meeting_completed_list.html", context)

def closeMeeting(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id)
    meeting.meetingState = MeetingState.모집완료.value
    meeting.save()
    return redirect('meeting_detail', meeting_id=meeting_id)

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