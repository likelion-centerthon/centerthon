from django.db import models
from enum import Enum
from user.models import User
from artist.models import Artist

# 미팅 모집 상태
class MeetingState (Enum):
    모집중 = '모집중'
    파토 = '파토'
    모집완료 = '모집완료'

#미팅 멤버 신청 상태
class MemberState(Enum):
    대기 = '대기'
    승인 = '승인'
    거부 = '거부'

# Create your models here.
class Meeting(models.Model):
    title = models.CharField(max_length=50) #제목
    body = models.TextField() #본문
    meetDate = models.DateField() #일시
    writeDate = models.DateTimeField(auto_now=True) #작성시간
    location = models.CharField(max_length=50) #장소
    age = models.CharField(max_length=10) #나이제한
    peopleNm = models.IntegerField() #인원
    kakaoLink = models.URLField() #카카오채팅방링크
    meetingState = models.CharField(max_length=20, choices=[(status.value, status.name) for status in MeetingState], default=MeetingState.모집중.value) #모집 상태
    image = models.ImageField(upload_to='meeting_images/', null=True, blank=True) #사진첨부
    writeUser = models.ForeignKey(User, on_delete=models.CASCADE,null=True) #작성자
    artist = models.ForeignKey(Artist, related_name="artist_meetings", on_delete=models.CASCADE)

class MeetingMember(models.Model):
    Meeting = models.ForeignKey(Meeting, related_name="members", on_delete=models.CASCADE, null=True) #참가미팅
    User = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    writeDate = models.DateTimeField(auto_now=True)  # 작성시간
    memberState = models.CharField(max_length=20, choices=[(status.value, status.name) for status in MemberState], default = MemberState.대기.value)
    def __str__(self):
        return self.User.userName

