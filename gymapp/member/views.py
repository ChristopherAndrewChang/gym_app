from django.shortcuts import render
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action

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
    search_fields = ['name', 'phone_number', 'email']

    @action(detail=False, methods=['post'])
    def scan_attendance(self, request):
        barcode = request.data.get("barcode")
        if not barcode:
            return Response({"error": "Barcode is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            member = Member.objects.get(barcode=barcode)

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
        

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all().order_by('-timestamp')
    serializer_class = AttendanceSerializer

    @action(detail=False, methods=['get'])
    def filter_by_date(self, request):
        """Filter attendance records by date (YYYY-MM-DD)"""
        date_str = request.query_params.get('date', None)  # Example: ?date=2025-03-26
        if date_str:
            filtered_attendance = Attendance.objects.filter(timestamp__date=date_str).order_by('-timestamp')
        else:
            filtered_attendance = Attendance.objects.all().order_by('-timestamp')

        serializer = AttendanceSerializer(filtered_attendance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)