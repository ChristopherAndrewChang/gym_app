from django.shortcuts import render
from rest_framework import viewsets, status, filters

from .models import MembershipType, Member
from .serializers import MembershipTypeSerializer, MemberSerializer
from member.tools.paginations import MembersPagination


class MembershipTypeViewSet(viewsets.ModelViewSet):
    queryset = MembershipType.objects.all()
    serializer_class = MembershipTypeSerializer


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    pagination_class = MembersPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'phone_number', 'email']
