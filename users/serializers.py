from rest_framework import serializers

from users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'password', 'telegram_id']
        extra_kwargs = {
            'password': {'write_only': True},
            'telegram_id': {'required': False},
        }

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            username=validated_data.get('username', ''),
            telegram_id=validated_data.get('telegram_id', '')
        )
        return user