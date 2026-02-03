from django.db import models

class UserProfile(models.Model):
    """Модель для хранения имён пользователей"""
    name = models.CharField(
        max_length=100,
        verbose_name="Имя"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"
        ordering = ['-created_at']
