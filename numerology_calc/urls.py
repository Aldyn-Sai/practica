from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Аутентификация
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
    
    # Сброс пароля
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='numerology_calc/auth/password_reset.html'
         ), 
         name='password_reset'),
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='numerology_calc/auth/password_reset_done.html'
         ), 
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='numerology_calc/auth/password_reset_confirm.html'
         ), 
         name='password_reset_confirm'),
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='numerology_calc/auth/password_reset_complete.html'
         ), 
         name='password_reset_complete'),
    
    # Главная и расчеты
    path('', views.HomeView.as_view(), name='home'),
    path('calculate/year/', views.calculate_year, name='calculate_year'),
    path('calculate/month/', views.calculate_month, name='calculate_month'),
    path('calculate/day/', views.calculate_day, name='calculate_day'),
    
    # API и дополнительные функции
    path('api/save-calculation/', views.save_calculation, name='save_calculation'),
    path('api/history/', views.get_calculations_history, name='get_history'),
    path('clear-history/', views.clear_history, name='clear_history'),
]