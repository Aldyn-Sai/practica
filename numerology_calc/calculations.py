from .data_descriptions import *

def reduce_to_single_digit(number):

    while number > 9:
        number = sum(int(digit) for digit in str(number))
    return number

def calculate_personal_year(birth_date, target_year):
    
   
    day_str = f"{birth_date.day:02d}"
    month_str = f"{birth_date.month:02d}"
    year_str = str(target_year)
    
   
    all_digits_str = day_str + month_str + year_str
    
   
    total_sum = sum(int(digit) for digit in all_digits_str)
    
   
    personal_year = reduce_to_single_digit(total_sum)
    
    return personal_year

def calculate_energy_year(birth_date, target_year):
   
    return calculate_personal_year(birth_date, target_year)

def calculate_personal_month(personal_year, month_number):
    """
    Рассчитывает персональное число месяца:
    Число года + номер месяца
    
    Пример: Число года 5 + месяц 3 (март) = 8
    Если больше 9: 5+12=17 → 1+7=8
    """
   
    month_sum = personal_year + month_number
    
    
    personal_month = reduce_to_single_digit(month_sum)
    
    return personal_month

def calculate_personal_day(target_date):
    """
    Рассчитывает число дня по формуле:
    Сумма всех цифр даты -> к однозначному
    
    Пример: 07.12.2025
    0+7+1+2+2+0+2+5 = 19 → 1+9 = 10 → 1+0 = 1
    """
   
    date_str = target_date.strftime("%d%m%Y")
    
    
    day_sum = sum(int(digit) for digit in date_str)
    
   
    personal_day = reduce_to_single_digit(day_sum)
    
    
    if personal_day == 10:
        personal_day = 1
    
    return personal_day

def get_year_description(personal_year):
    """Получает описание для персонального года"""
    return YEAR_DESCRIPTIONS.get(personal_year, {
        'title': f"Год числа «{personal_year}»",
        'short': "Информация отсутствует",
        'full': "Описание для этого числа года пока не добавлено."
    })

def get_energy_description(energy_year):
    """Получает описание для энергии года"""
    return ENERGY_DESCRIPTIONS.get(energy_year, {
        'title': f"Энергия {energy_year}",
        'short': "Информация отсутствует",
        'full': "Описание для этой энергии года пока не добавлено."
    })

def get_month_description(personal_month):
    """Получает описание для месяца"""
    return MONTH_DESCRIPTIONS.get(personal_month, {
        'title': f"Месяц числа {personal_month}",
        'short': "Информация отсутствует",
        'full': "Описание для этого числа месяца пока не добавлено."
    })

def get_day_description(personal_day):
    """Получает описание для дня"""
    return DAY_DESCRIPTIONS.get(personal_day, {
        'title': f"День числа {personal_day}",
        'short': "Информация отсутствует",
        'full': "Описание для этого числа дня пока не добавлено."
    })

def get_month_name(month_number):
    """Получает название месяца по номеру"""
    return MONTH_NAMES.get(month_number, f"Месяц {month_number}")

def get_detailed_calculation(birth_date, target_year):
    """
    Возвращает подробный расчет с шагами для года
    """
  
    day_str = f"{birth_date.day:02d}"
    month_str = f"{birth_date.month:02d}"
    year_str = str(target_year)
    
    all_digits = day_str + month_str + year_str
    digits_list = [int(d) for d in all_digits]
    
    
    day_sum = sum(int(d) for d in day_str)
    month_sum = sum(int(d) for d in month_str)
    year_sum = sum(int(d) for d in year_str)
    total_sum = sum(digits_list)
    
   
    result = reduce_to_single_digit(total_sum)
    
    
    calculation_steps = [
        f"День рождения: {day_str} → {'+'.join(day_str)} = {day_sum}",
        f"Месяц рождения: {month_str} → {'+'.join(month_str)} = {month_sum}",
        f"Целевой год: {year_str} → {'+'.join(year_str)} = {year_sum}",
        f"Общая сумма: {'+'.join(all_digits)} = {total_sum}",
    ]
    
   
    if total_sum > 9:
        reduction = reduce_to_single_digit(total_sum)
        if reduction != total_sum:
            reduction_steps = []
            current = total_sum
            while current > 9:
                current_str = str(current)
                current_digits = [int(d) for d in current_str]
                next_sum = sum(current_digits)
                reduction_steps.append(f"{current} → {'+'.join(current_str)} = {next_sum}")
                current = next_sum
            calculation_steps.append(f"Приводим к однозначному: {' → '.join(reduction_steps)} = {result}")
    
    return {
        'birth_date': birth_date,
        'target_year': target_year,
        'day_str': day_str,
        'month_str': month_str,
        'year_str': year_str,
        'all_digits': all_digits,
        'digits_list': digits_list,
        'day_sum': day_sum,
        'month_sum': month_sum,
        'year_sum': year_sum,
        'total_sum': total_sum,
        'result': result,
        'steps': calculation_steps,
        'formula_display': f"{'+'.join(all_digits)} = {total_sum} → {result}"
    }