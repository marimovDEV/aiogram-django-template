from django.db import models

class TelegramUser(models.Model):
    telegram_id = models.BigIntegerField(unique=True, verbose_name="Telegram ID")
    full_name = models.CharField(max_length=255, verbose_name="To'liq ism")
    username = models.CharField(max_length=255, null=True, blank=True, verbose_name="Username")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Qo'shilgan vaqti")

    def __str__(self):
        return f"{self.full_name} ({self.telegram_id})"

    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"
