from rest_framework import serializers
from .models import MembershipType, Member


class MembershipTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembershipType
        fields = '__all__'  # Includes all fields in the model


class MemberSerializer(serializers.ModelSerializer):
    membership_type = MembershipTypeSerializer(read_only=True)

    membership_type_id = serializers.PrimaryKeyRelatedField(
        queryset=MembershipType.objects.all(), source='membership_type', write_only=True
    )

    class Meta:
        model = Member
        fields = '__all__'