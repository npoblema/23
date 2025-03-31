from rest_framework import serializers
from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = ['id', 'user', 'place', 'time', 'action', 'is_pleasant', 'related_habit', 'periodicity', 'reward', 'duration', 'is_public']
        read_only_fields = ['user']  # Поле только для чтения

    def validate(self, data):
        # Твоя логика валидации
        if data.get('duration', 0) > 120:
            raise serializers.ValidationError("Время выполнения не должно превышать 120 секунд")
        if data.get('reward') and data.get('related_habit'):
            raise serializers.ValidationError("Нельзя указать одновременно вознаграждение и связанную привычку")
        return data

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)