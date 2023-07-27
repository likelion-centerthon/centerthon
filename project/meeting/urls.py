from django.contrib import admin
from django.urls import path
from .views import CreateMeeting, MeetingDtl,MeetingList,closeMeeting,MeetingCloseList,applyMeeting,editMeeting

urlpatterns = [
    path('<int:artist_id>/',MeetingList, name="MeetingList"),
    path('<int:artist_id>/completed/',MeetingCloseList,name="MeetingCloseList"),
    path('<int:artist_id>/create/', CreateMeeting , name="createMeeting"),
    path('dtl/<int:meeting_id>/', MeetingDtl, name='meeting_detail'),
    path('meeting/<int:meeting_id>/close/', closeMeeting, name='closeMeeting'),
    path('meeting/<int:meeting_id>/apply/', applyMeeting, name='applyMeeting'),
    path('<int:meeting_id>/edit', editMeeting, name='editMeeting'),

]