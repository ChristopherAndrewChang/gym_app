from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MembershipTypeViewSet, MemberViewSet

router = DefaultRouter()
router.register(r'members', MemberViewSet)
router.register(r'membership-types', MembershipTypeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
