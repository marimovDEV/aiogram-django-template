from django.contrib import admin
from .models import TelegramUser

@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'telegram_id', 'full_name', 'username', 'created_at']
    search_fields = ['full_name', 'username', 'telegram_id']
