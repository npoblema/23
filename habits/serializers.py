from rest_framework import serializers

from habits.models import Habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = ['id', 'user', 'place', 'time', 'action', 'is_pleasant', 'related_habit', 'periodicity', 'reward', 'duration', 'is_public']
        read_only_fields = ['user']

    def validate(self, data):
        # Исключить одновременный выбор related_habit и reward
        if data.get('related_habit') and data.get('reward'):
            raise serializers.ValidationError("Нельзя одновременно указывать связанную привычку и вознаграждение.")

        # Время выполнения не больше 120 секунд
        if data.get('duration', 0) > 120:
            raise serializers.ValidationError("Время выполнения не должно превышать 120 секунд.")

        # Связанная привычка должна быть приятной
        if data.get('related_habit') and not data['related_habit'].is_pleasant:
            raise serializers.ValidationError("Связанная привычка должна быть приятной (is_pleasant=True).")

        # У приятной привычки не может быть reward или related_habit
        if data.get('is_pleasant'):
            if data.get('reward'):
                raise serializers.ValidationError("У приятной привычки не может быть вознаграждения.")
            if data.get('related_habit'):
                raise serializers.ValidationError("У приятной привычки не может быть связанной привычки.")

        # Периодичность от 1 до 7 дней
        periodicity = data.get('periodicity', 1)
        if periodicity < 1 or periodicity > 7:
            raise serializers.ValidationError("Периодичность должна быть от 1 до 7 дней.")

        return data