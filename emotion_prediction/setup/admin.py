from django.contrib import admin
from .models import Users, Emotion, Story, AnalyzedStory
# Register your models here.

@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ("id", "last_name", "first_name", "email",)
    search_fields = ("id", "last_name", "first_name", "email",)


@admin.register(Emotion)
class EmotionAdmin(admin.ModelAdmin):
    list_display = ("id", "emotion",)
    search_fields = ("id", "emotion",)


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ("id", "story",)
    search_fields = ("id", "story",)


@admin.register(AnalyzedStory)
class AnalyzedStoryAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "phrase", "analyzed_emotion",)
    search_fields = ("id", "user__last_name", "user__first_name", "phrase__story", "analyzed_emotion__emotion")
