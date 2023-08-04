from django import forms
from .models import Meeting

class MeetingEditForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ['title', 'body', 'meetDate', 'location', 'age', 'peopleNm', 'kakaoLink', 'image']
