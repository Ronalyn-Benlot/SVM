from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Users(models.Model):
    account = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    username = models.CharField(unique=True, max_length=30)
    password = models.CharField(max_length=100)
    last_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)

    def __str__(self):
            return f"{self.last_name.upper()}, {self.first_name.title()}"

    def full_name(self):
        return f"{self.last_name.upper()}, {self.first_name.title()}"

    class Meta:
        verbose_name_plural = "users"

class Emotion(models.Model):
     emotion = models.CharField(max_length=20)
     
     def __str__(self):
          return f"{self.emotion}"

     class Meta:
          verbose_name_plural = "emotions"

class Story(models.Model):
     story = models.TextField()
     
     def __str__(self):
          return f"{self.story}"
     
     class Meta:
          verbose_name_plural = "stories"

class AnalyzedStory(models.Model):
     user = models.ForeignKey(Users, on_delete=models.CASCADE)
     phrase = models.ForeignKey(Story, on_delete=models.CASCADE)
     fear = models.FloatField(default=None, null=True, blank=True)
     anger = models.FloatField(default=None, null=True, blank=True)
     joy = models.FloatField(default=None, null=True, blank=True)
     sadness = models.FloatField(default=None, null=True, blank=True)
     disgust = models.FloatField(default=None, null=True, blank=True)
     surprise = models.FloatField(default=None, null=True, blank=True)
     analyzed_emotion = models.ForeignKey(Emotion, on_delete=models.CASCADE)
     
     def __str__(self):
          return f"{self.user.last_name}, {self.user.first_name}"
     
     class Meta:
          verbose_name_plural = "analyzed stories"
    
