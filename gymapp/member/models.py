from django.db import models
from django.db import models
import uuid
import random
import string
from django.db import models
from django.utils.timezone import now
from datetime import timedelta
from dateutil.relativedelta import relativedelta


class MembershipType(models.Model):
    type = models.CharField(max_length=200)
    description = models.TextField(max_length=500, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.type


class Member(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    phone_number = models.CharField(max_length=30)
    email = models.CharField(max_length=255)
    address = models.TextField(null=True, blank=True)
    barcode = models.CharField(max_length=50, unique=True, blank=True, null=True)
    expiry = models.DateField(null=True, blank=True)
    credit = models.IntegerField(null=True, blank=True)
    
    membership_type = models.ForeignKey(MembershipType, on_delete=models.SET_NULL, null=True)

    def generate_qr(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))

    def save(self, *args, **kwargs):
        if not self.expiry:
            self.expiry = now().date() + relativedelta(months=1)
        
        if not self.barcode:
            self.barcode = self.generate_qr()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Attendance(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.member.name} - {self.timestamp}"