from django import forms

class NameForm(forms.Form):
    """Форма для ввода имени"""
    name = forms.CharField(
        max_length=100,
        label="Имя",
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите ваше имя...',
            'required': True
        })
    )
    
    def clean_name(self):
        """Валидация поля имени"""
        name = self.cleaned_data.get('name')
        
        # Убираем лишние пробелы
        name = name.strip()
        
        # Проверка на пустое имя
        if not name:
            raise forms.ValidationError("Имя не может быть пустым")
        
        # Проверка на минимальную длину
        if len(name) < 2:
            raise forms.ValidationError("Имя должно содержать хотя бы 2 символа")
        
        # Проверка на цифры в имени
        if any(char.isdigit() for char in name):
            raise forms.ValidationError("Имя не должно содержать цифр")
        
        return name