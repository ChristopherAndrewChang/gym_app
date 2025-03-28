from rest_framework import serializers
from .models import MembershipType

class MembershipTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembershipType
        fields = '__all__'  # Includes all fields in the model
