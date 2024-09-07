from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import CustomUser, CrushRequest, Confession, Message, Notification

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_superuser', 'is_active')

@admin.register(CrushRequest)
class CrushRequestAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'is_matched', 'is_denied', 'date_sent')
    list_filter = ('is_matched', 'is_denied')
    search_fields = ('sender__username', 'receiver__username')

@admin.register(Confession)
class ConfessionAdmin(admin.ModelAdmin):
    list_display = ('author', 'text', 'is_anonymous', 'created_at')
    list_filter = ('is_anonymous', 'created_at')
    search_fields = ('text', 'author__username')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'content', 'timestamp')
    search_fields = ('sender__username', 'receiver__username', 'content')
    list_filter = ('timestamp',)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'read', 'created_at')
    list_filter = ('read', 'created_at')
    search_fields = ('user__username', 'text')

