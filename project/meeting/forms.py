from django import forms
from .models import Meeting

class MeetingEditForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ['title', 'body', 'meetDate', 'location', 'age', 'peopleNm', 'kakaoLink', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.meetDate:  # meetDate 필드에 값이 있는 경우
            self.initial['meetDate'] = self.instance.meetDate.strftime('%Y-%m-%d')