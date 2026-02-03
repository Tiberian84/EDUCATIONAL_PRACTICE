from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserProfile
from .forms import NameForm

def home(request):
    """
    Главная страница с формой ввода имени.
    Обрабатывает GET и POST запросы.
    """
    # Получаем последние 10 пользователей
    recent_users = UserProfile.objects.all()[:10]
    
    if request.method == 'POST':
        form = NameForm(request.POST)
        
        if form.is_valid():
            # Получаем имя из формы
            name = form.cleaned_data['name']
            
            # Сохраняем в базу данных
            UserProfile.objects.create(name=name)
            
            # Перенаправляем на главную страницу с именем в параметрах
            return render(request, 'greetings/home.html', {
                'name': name,
                'recent_users': recent_users,
                'form': form
            })
    else:
        form = NameForm()
    
    return render(request, 'greetings/home.html', {
        'form': form,
        'recent_users': recent_users
    })