from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MembershipTypeViewSet

router = DefaultRouter()
router.register(r'membership-types', MembershipTypeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
