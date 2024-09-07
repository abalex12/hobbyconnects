from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    preferences = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.email.endswith('@cgu-odisha.ac.in'):
            raise ValueError("Email must be from the domain @cgu-odisha.ac.in")
        super().save(*args, **kwargs)

class CrushRequest(models.Model):
    sender = models.ForeignKey(CustomUser, related_name='sent_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, related_name='received_requests', on_delete=models.CASCADE)
    is_matched = models.BooleanField(default=False)
    is_denied = models.BooleanField(default=False)
    date_sent = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('sender', 'receiver')
        ordering = ['-date_sent']

class Confession(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    text = models.TextField()
    is_anonymous = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

class Message(models.Model):
    sender = models.ForeignKey(CustomUser, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
