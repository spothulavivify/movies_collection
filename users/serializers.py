from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    access_token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'access_token')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        refresh = RefreshToken.for_user(user)
        validated_data['access_token'] = str(refresh.access_token)
        return validated_data