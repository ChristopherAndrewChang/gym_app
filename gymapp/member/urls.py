from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MembershipTypeViewSet, MemberViewSet, AttendanceViewSet

router = DefaultRouter()
router.register(r'members', MemberViewSet)
router.register(r'membership-types', MembershipTypeViewSet)
router.register(r'attendance', AttendanceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
