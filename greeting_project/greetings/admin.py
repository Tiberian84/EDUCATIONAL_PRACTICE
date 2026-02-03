from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']  # Поля для отображения в списке
    search_fields = ['name']                # Поиск по имени
    ordering = ['-created_at']              # Сортировка по дате (новые сверху)
    list_filter = ['created_at']            # Фильтр по дате
    
    # Заголовки в админке
    verbose_name = "Профиль пользователя"
    verbose_name_plural = "Профили пользователей"