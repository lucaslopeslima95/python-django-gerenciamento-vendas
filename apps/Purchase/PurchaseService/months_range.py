from datetime import datetime
import calendar

def current_month_range():
    """Obtém a quantidade de dias do mês atual.

    Retorna o número de dias do mês atual com base na data atual.

    Returns:
        int: Número de dias do mês atual.
    """
    current_month = datetime.now().month
    current_year = datetime.now().year
    number_of_days = calendar.monthrange(current_year, current_month)[1]
    
    return number_of_days


def next_month_range():
    """Obtém a quantidade de dias do próximo mês.

    Retorna o número de dias do próximo mês com base na data atual.

    Returns:
        int: Número de dias do próximo mês.
    """
    next_month = datetime.now().month
    next_year = datetime.now().year
    
    if next_month > 12:
        next_month = 1
        next_year += 1
        
    number_of_days = calendar.monthrange(next_year, (next_month+1))[1]
    return number_of_days