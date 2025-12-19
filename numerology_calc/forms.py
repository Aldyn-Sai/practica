from django import forms
from datetime import date

class YearCalculationForm(forms.Form):
    """Форма для расчета года"""
    birth_date = forms.DateField(
        label='Дата рождения',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control mystic-input'}),
        required=True
    )
    
    target_year = forms.IntegerField(
        label='Год для расчета',
        min_value=1900,
        max_value=2100,
        initial=date.today().year,
        widget=forms.NumberInput(attrs={'class': 'form-control mystic-input'}),
        required=True
    )

class MonthCalculationForm(forms.Form):
    """Форма для расчета месяца"""
    personal_year = forms.IntegerField(
        label='Ваше персональное число года',
        min_value=1,
        max_value=9,
        widget=forms.NumberInput(attrs={'class': 'form-control mystic-input'}),
        required=True,
        help_text='Если вы его не знаете, сначала рассчитайте прогноз на год'
    )
    
    month = forms.ChoiceField(
        label='Месяц',
        choices=[(i, f'{i} - {name}') for i, name in [
            (1, 'Январь'), (2, 'Февраль'), (3, 'Март'), (4, 'Апрель'),
            (5, 'Май'), (6, 'Июнь'), (7, 'Июль'), (8, 'Август'),
            (9, 'Сентябрь'), (10, 'Октябрь'), (11, 'Ноябрь'), (12, 'Декабрь')
        ]],
        widget=forms.Select(attrs={'class': 'form-control mystic-input'}),
        required=True
    )

class DayCalculationForm(forms.Form):
    """Форма для расчета дня"""
    target_date = forms.DateField(
        label='Дата для расчета',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control mystic-input'}),
        initial=date.today(),
        required=True
    )
    from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date
import re

class CustomUserCreationForm(UserCreationForm):
    """Кастомная форма регистрации"""
    email = forms.EmailField(
        label='Email',
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control mystic-input',
            'placeholder': 'your@email.com'
        })
    )
    
    username = forms.CharField(
        label='Имя пользователя',
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control mystic-input',
            'placeholder': 'Придумайте имя пользователя'
        }),
        help_text='Только буквы, цифры и @/./+/-/_'
    )
    
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control mystic-input',
            'placeholder': 'Не менее 8 символов'
        })
    )
    
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control mystic-input',
            'placeholder': 'Повторите пароль'
        })
    )
    
    birth_date = forms.DateField(
        label='Дата рождения (необязательно)',
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control mystic-input'
        })
    )
    
    agree_terms = forms.BooleanField(
        label='Я согласен с условиями использования',
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input mystic-checkbox'
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'birth_date')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Этот email уже используется')
        return email
    
    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        if birth_date:
            if birth_date > date.today():
                raise ValidationError('Дата рождения не может быть в будущем')
            age = date.today().year - birth_date.year
            if age < 13:
                raise ValidationError('Вам должно быть не менее 13 лет')
        return birth_date

class CustomAuthenticationForm(AuthenticationForm):
    """Кастомная форма входа"""
    username = forms.CharField(
        label='Имя пользователя или Email',
        widget=forms.TextInput(attrs={
            'class': 'form-control mystic-input',
            'placeholder': 'Введите имя пользователя или email'
        })
    )
    
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control mystic-input',
            'placeholder': 'Введите пароль'
        })
    )
    
    remember_me = forms.BooleanField(
        label='Запомнить меня',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input mystic-checkbox'
        })
    )
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Проверяем, является ли ввод email
        if '@' in username:
            try:
                user = User.objects.get(email=username)
                return user.username
            except User.DoesNotExist:
                raise ValidationError('Пользователь с таким email не найден')
        return username

class PasswordResetRequestForm(forms.Form):
    """Форма запроса сброса пароля"""
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control mystic-input',
            'placeholder': 'Введите ваш email'
        })
    )

class PasswordResetConfirmForm(forms.Form):
    """Форма подтверждения сброса пароля"""
    new_password1 = forms.CharField(
        label='Новый пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control mystic-input'
        })
    )
    
    new_password2 = forms.CharField(
        label='Подтверждение нового пароля',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control mystic-input'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('new_password1')
        password2 = cleaned_data.get('new_password2')
        
        if password1 and password2 and password1 != password2:
            raise ValidationError('Пароли не совпадают')
        
        return cleaned_data

# Остальные формы остаются теми же
class YearCalculationForm(forms.Form):
    """Форма для расчета года"""
    birth_date = forms.DateField(
        label='Дата рождения',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control mystic-input'}),
        required=True
    )
    
    target_year = forms.IntegerField(
        label='Год для расчета',
        min_value=1900,
        max_value=2100,
        initial=date.today().year,
        widget=forms.NumberInput(attrs={'class': 'form-control mystic-input'}),
        required=True
    )

class MonthCalculationForm(forms.Form):
    """Форма для расчета месяца"""
    personal_year = forms.IntegerField(
        label='Ваше персональное число года',
        min_value=1,
        max_value=9,
        widget=forms.NumberInput(attrs={'class': 'form-control mystic-input'}),
        required=True,
        help_text='Если вы его не знаете, сначала рассчитайте прогноз на год'
    )
    
    month = forms.ChoiceField(
        label='Месяц',
        choices=[(i, f'{i} - {name}') for i, name in [
            (1, 'Январь'), (2, 'Февраль'), (3, 'Март'), (4, 'Апрель'),
            (5, 'Май'), (6, 'Июнь'), (7, 'Июль'), (8, 'Август'),
            (9, 'Сентябрь'), (10, 'Октябрь'), (11, 'Ноябрь'), (12, 'Декабрь')
        ]],
        widget=forms.Select(attrs={'class': 'form-control mystic-input'}),
        required=True
    )

class DayCalculationForm(forms.Form):
    """Форма для расчета дня"""
    target_date = forms.DateField(
        label='Дата для расчета',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control mystic-input'}),
        initial=date.today(),
        required=True
    )