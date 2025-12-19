from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import TemplateView
from django.views.decorators.http import require_POST
from datetime import date
import json

from .decorators import login_required_message
from .forms import (
    CustomUserCreationForm, CustomAuthenticationForm,
    PasswordResetRequestForm, PasswordResetConfirmForm,
    YearCalculationForm, MonthCalculationForm, DayCalculationForm
)
from .calculations import (
    calculate_personal_year, calculate_energy_year,
    calculate_personal_month, calculate_personal_day,
    get_year_description, get_energy_description,
    get_month_description, get_day_description,
    get_month_name, get_detailed_calculation
)

# ==================== АУТЕНТИФИКАЦИЯ ====================

def register_view(request):
    """Регистрация нового пользователя"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Сохраняем дату рождения в профиль
            birth_date = form.cleaned_data.get('birth_date')
            if birth_date:
                user.profile.birth_date = birth_date
                user.profile.save()
            
            # Автоматический вход после регистрации
            login(request, user)
            
            messages.success(request, 'Добро пожаловать! Ваш магический аккаунт создан.')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'numerology_calc/auth/register.html', {'form': form})

def login_view(request):
    """Вход в систему"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get('remember_me', False)
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                
                # Настройка запоминания сессии
                if not remember_me:
                    request.session.set_expiry(0)  # Сессия закроется при закрытии браузера
                
                messages.success(request, f'Добро пожаловать, {user.username}!')
                
                # Перенаправление на следующую страницу или домой
                next_page = request.GET.get('next', 'home')
                return redirect(next_page)
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'numerology_calc/auth/login.html', {'form': form})

@login_required_message
def logout_view(request):
    """Выход из системы"""
    logout(request)
    messages.info(request, 'Вы успешно вышли из системы.')
    return redirect('home')

@login_required_message
def profile_view(request):
    """Профиль пользователя"""
    return render(request, 'numerology_calc/auth/profile.html')

@login_required_message
def profile_edit_view(request):
    """Редактирование профиля"""
    if request.method == 'POST':
        # Обработка формы редактирования профиля
        pass
    return render(request, 'numerology_calc/auth/profile_edit.html')

def password_reset_view(request):
    """Запрос сброса пароля"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            # Отправка email для сброса пароля
            messages.success(request, 'Инструкции по сбросу пароля отправлены на ваш email.')
            return redirect('login')
    else:
        form = PasswordResetRequestForm()
    
    return render(request, 'numerology_calc/auth/password_reset.html', {'form': form})

# ==================== РАСЧЕТЫ ====================

class HomeView(TemplateView):
    """Главная страница"""
    template_name = 'numerology_calc/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Автозаполнение даты рождения из профиля
        initial_data = {}
        if self.request.user.is_authenticated and self.request.user.profile.birth_date:
            initial_data['birth_date'] = self.request.user.profile.birth_date
        
        context['year_form'] = YearCalculationForm(initial=initial_data)
        context['month_form'] = MonthCalculationForm()
        context['day_form'] = DayCalculationForm()
        
        # Статистика для залогиненных пользователей
        if self.request.user.is_authenticated:
            context['user_calculations'] = self.request.user.profile.calculations_count
        
        return context

@login_required_message
def calculate_year(request):
    """Расчет прогноза на год"""
    if request.method == 'POST':
        form = YearCalculationForm(request.POST)
        if form.is_valid():
            birth_date = form.cleaned_data['birth_date']
            target_year = form.cleaned_data['target_year']
            
            # Выполняем расчеты
            personal_year = calculate_personal_year(birth_date, target_year)
            energy_year = calculate_energy_year(birth_date, target_year)
            
            # Получаем описания
            year_desc = get_year_description(personal_year)
            energy_desc = get_energy_description(energy_year)
            
            # Детальный расчет для показа
            detailed_calc = get_detailed_calculation(birth_date, target_year)
            
            # Увеличиваем счетчик расчетов
            request.user.profile.increment_calculations()
            
            # Сохраняем расчет в сессии (можно и в БД)
            calculation_data = {
                'type': 'year',
                'birth_date': birth_date.strftime('%Y-%m-%d'),
                'target_year': target_year,
                'result': personal_year,
                'timestamp': date.today().strftime('%Y-%m-%d')
            }
            
            # Сохраняем в сессии
            if 'calculations_history' not in request.session:
                request.session['calculations_history'] = []
            
            request.session['calculations_history'].append(calculation_data)
            request.session.modified = True
            
            context = {
                'birth_date': birth_date,
                'target_year': target_year,
                'personal_year': personal_year,
                'energy_year': energy_year,
                'year_description': year_desc,
                'energy_description': energy_desc,
                'detailed_calculation': detailed_calc,
                'form': form,
            }
            
            return render(request, 'numerology_calc/year_result.html', context)
    else:
        # Автозаполнение даты рождения из профиля
        initial_data = {}
        if request.user.is_authenticated and request.user.profile.birth_date:
            initial_data['birth_date'] = request.user.profile.birth_date
        
        form = YearCalculationForm(initial=initial_data)
    
    return render(request, 'numerology_calc/home.html', {'year_form': form})

@login_required_message
def calculate_month(request):
    """Расчет прогноза на месяц"""
    if request.method == 'POST':
        form = MonthCalculationForm(request.POST)
        if form.is_valid():
            personal_year = form.cleaned_data['personal_year']
            month_number = int(form.cleaned_data['month'])
            
            # Выполняем расчет
            personal_month = calculate_personal_month(personal_year, month_number)
            
            # Получаем описание
            month_desc = get_month_description(personal_month)
            month_name = get_month_name(month_number)
            
            # Детальный расчет
            detailed_steps = [
                f"Ваше персональное число года: {personal_year}",
                f"Номер месяца: {month_number}",
                f"Сумма: {personal_year} + {month_number} = {personal_year + month_number}",
                f"Приводим к однозначному: {personal_year + month_number} → {personal_month}"
            ]
            
            # Увеличиваем счетчик расчетов
            request.user.profile.increment_calculations()
            
            # Сохраняем расчет
            calculation_data = {
                'type': 'month',
                'personal_year': personal_year,
                'month': month_number,
                'result': personal_month,
                'timestamp': date.today().strftime('%Y-%m-%d')
            }
            
            if 'calculations_history' not in request.session:
                request.session['calculations_history'] = []
            
            request.session['calculations_history'].append(calculation_data)
            request.session.modified = True
            
            context = {
                'personal_year': personal_year,
                'month_number': month_number,
                'month_name': month_name,
                'personal_month': personal_month,
                'month_description': month_desc,
                'detailed_steps': detailed_steps,
                'form': form,
            }
            
            return render(request, 'numerology_calc/month_result.html', context)
    else:
        form = MonthCalculationForm()
    
    return render(request, 'numerology_calc/home.html', {'month_form': form})

@login_required_message
def calculate_day(request):
    """Расчет прогноза на день"""
    if request.method == 'POST':
        form = DayCalculationForm(request.POST)
        if form.is_valid():
            target_date = form.cleaned_data['target_date']
            
            # Выполняем расчет
            personal_day = calculate_personal_day(target_date)
            
            # Получаем описание
            day_desc = get_day_description(personal_day)
            
            # Детальный расчет
            date_str = target_date.strftime("%d%m%Y")
            digits = [int(d) for d in date_str]
            digit_sum = sum(digits)
            
            detailed_steps = [
                f"Выбранная дата: {target_date.strftime('%d.%m.%Y')}",
                f"Цифры даты: {date_str} → {'+'.join(str(d) for d in digits)} = {digit_sum}",
                f"Приводим к однозначному: {digit_sum} → {personal_day}"
            ]
            
            # Увеличиваем счетчик расчетов
            request.user.profile.increment_calculations()
            
            # Сохраняем расчет
            calculation_data = {
                'type': 'day',
                'target_date': target_date.strftime('%Y-%m-%d'),
                'result': personal_day,
                'timestamp': date.today().strftime('%Y-%m-%d')
            }
            
            if 'calculations_history' not in request.session:
                request.session['calculations_history'] = []
            
            request.session['calculations_history'].append(calculation_data)
            request.session.modified = True
            
            context = {
                'target_date': target_date,
                'personal_day': personal_day,
                'day_description': day_desc,
                'detailed_steps': detailed_steps,
                'form': form,
            }
            
            return render(request, 'numerology_calc/day_result.html', context)
    else:
        form = DayCalculationForm()
    
    return render(request, 'numerology_calc/home.html', {'day_form': form})

# ==================== API И ДОПОЛНИТЕЛЬНЫЕ ФУНКЦИИ ====================

@login_required_message
def save_calculation(request):
    """Сохранение расчета в избранное"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Логика сохранения расчета
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

@login_required_message
def get_calculations_history(request):
    """Получение истории расчетов"""
    history = request.session.get('calculations_history', [])
    return JsonResponse({'history': history})

@login_required_message
def clear_history(request):
    """Очистка истории расчетов"""
    if 'calculations_history' in request.session:
        del request.session['calculations_history']
        request.session.modified = True
    return redirect('profile')