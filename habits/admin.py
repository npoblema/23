from django.contrib import admin

from habits.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'time', 'place', 'is_public')
    list_filter = ('is_public', 'user')
    search_fields = ('action', 'place')