from django.contrib import admin
from django.urls import path
from .views import CreateMeeting, MeetingDtl,MeetingList,closeMeeting,MeetingCloseList,applyMeeting,editMeeting,writedMeetingList,memberStateAccept, memberStateRefusal,applyedMeetingList,subPNList, MeetingList_tutorial

app_name = "meeting"

urlpatterns = [
    path('<int:artist_id>/',MeetingList, name="MeetingList"),
    path('<int:artist_id>/completed/',MeetingCloseList,name="MeetingCloseList"),
    path('<int:artist_id>/create/', CreateMeeting , name="createMeeting"),
    path('<int:artist_id>/<int:meeting_id>/dtl', MeetingDtl, name='meeting_detail'),
    path('<int:artist_id>/<int:meeting_id>/close/', closeMeeting, name='closeMeeting'),
    path('<int:artist_id>/<int:meeting_id>/apply/', applyMeeting, name='applyMeeting'),
    path('<int:artist_id>/<int:meeting_id>/edit', editMeeting, name='editMeeting'),
    path('<int:artist_id>/write/',writedMeetingList,name='writedMeetingList'),
    path('<int:artist_id>/write/<int:meetingMember_id>/accept',memberStateAccept,name='memberStateAccept'),
    path('<int:artist_id>/write/<int:meetingMember_id>/refusal', memberStateRefusal, name='memberStateRefusal'),
    path('<int:artist_id>/apply/', applyedMeetingList, name='applyedMeetingList'),
    path('<int:artist_id>/phone/', subPNList, name='subPNList'),
    path('<int:artist_id>/tutorial/', MeetingList_tutorial, name =' MeetingList_tutorial'),

]