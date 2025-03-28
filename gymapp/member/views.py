from django.shortcuts import render
from rest_framework import viewsets, status, filters

from .models import MembershipType
from .serializers import MembershipTypeSerializer


class MembershipTypeViewSet(viewsets.ModelViewSet):
    queryset = MembershipType.objects.all()
    serializer_class = MembershipTypeSerializer

