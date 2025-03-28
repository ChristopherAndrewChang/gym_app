from django.shortcuts import render
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils.timezone import now
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination

from .models import MembershipType, Member, Attendance
from .serializers import MembershipTypeSerializer, MemberSerializer, AttendanceSerializer
from member.tools.paginations import MembersPagination


class MembershipTypeViewSet(viewsets.ModelViewSet):
    queryset = MembershipType.objects.all()
    serializer_class = MembershipTypeSerializer


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    pagination_class = MembersPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'phone_number', 'email', 'status']

    @action(detail=False, methods=['post'])
    def scan_attendance(self, request):
        barcode = request.data.get("barcode")
        if not barcode:
            return Response({"error": "Barcode is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            member = Member.objects.get(barcode=barcode)

            # Check if the member status is expired
            if getattr(member, 'status', '') == "expired":
                return Response({"error": "Membership is expired!"}, status=status.HTTP_400_BAD_REQUEST)
            
            has_attended_today = Attendance.objects.filter(
                member=member, timestamp__date=now().date()
            ).exists()

            if has_attended_today:
                return Response({"error": "Member has already attended a session today!"}, status=status.HTTP_400_BAD_REQUEST)


            # Check if the member has credits left
            if member.credit and member.credit > 0:
                # Deduct one session and record attendance
                member.credit -= 1
                member.save()

                attendance = Attendance.objects.create(member=member)

                return Response({
                    "message": "Attendance recorded successfully",
                    "member": MemberSerializer(member).data,
                    "attendance": AttendanceSerializer(attendance).data
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "No remaining session credits"}, status=status.HTTP_400_BAD_REQUEST)

        except Member.DoesNotExist:
            return Response({"error": "Member not found"}, status=status.HTTP_404_NOT_FOUND)
    

    @action(detail=False, methods=['get'])
    def low_credit_members(self, request):
        """Fetch members with 2 or fewer session credits left (Paginated)"""
        filtered_members = Member.objects.filter(credit__lte=2).order_by('-credit')  # Sort by credit for better display

        # Apply DRF pagination manually
        page = self.paginate_queryset(filtered_members)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(filtered_members, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all().order_by('-timestamp')
    serializer_class = AttendanceSerializer
    pagination_class = MembersPagination
    filter_backends = [filters.SearchFilter]
    filterset_fields = ['timestamp']
    search_fields = ['member__name']

    def list(self, request, *args, **kwargs):
        """Get all attendance with optional date filtering"""
        date_str = request.query_params.get('date', None)  # Example: ?date=2025-03-26
        
        if date_str:
            self.queryset = self.queryset.filter(timestamp__date=date_str)

        return super().list(request, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def filter_by_date(self, request):
        """Filter attendance records by date (YYYY-MM-DD) with pagination"""
        date_str = request.query_params.get('date', None)  # Example: ?date=2025-03-26

        if date_str:
            filtered_attendance = Attendance.objects.filter(timestamp__date=date_str).order_by('-timestamp')
        else:
            filtered_attendance = Attendance.objects.all().order_by('-timestamp')

        # Apply DRF pagination manually
        page = self.paginate_queryset(filtered_attendance)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(filtered_attendance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)