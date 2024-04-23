from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User authorising and register.
    """

    class Meta:
        model = User
        fields = ('phone_number', 'pass_code',)


class ReferralSerializer(serializers.ModelSerializer):
    """
    Serializer for referrals list.
    """
    class Meta:
        model = User
        fields = ('phone_number',)


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the User profile.
    """
    referrals = ReferralSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('phone_number', 'referral_code', 'referrals', 'referred_code')


class CodeProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for entering referral code.
    """

    class Meta:
        model = User
        fields = ('referral_code',)
