from django.contrib import admin

# Register your models here.

from .models import Member, MembershipType, Attendance

admin.site.register(Member)
admin.site.register(MembershipType)
admin.site.register(Attendance)