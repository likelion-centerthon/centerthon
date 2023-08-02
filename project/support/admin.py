from django.contrib import admin

from support.models import Support, SupportForm, Bank

# Register your models here.
admin.site.register(Support)
admin.site.register(SupportForm)
admin.site.register(Bank)