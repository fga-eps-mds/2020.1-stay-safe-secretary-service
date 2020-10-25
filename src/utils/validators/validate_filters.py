import datetime

from utils.constants import VALID_CRIMES_DF, VALID_CRIMES_SP

def validade_crime_filters(params, per_capita):
    secretary = params.get('secretary')
    crime = params.get('nature')
    initial_month = params.get('initial_month')
    final_month = params.get('final_month')

    if secretary is None:
        return "Parâmetro secretary obrigatório."

    if secretary not in ['sp', 'df']:
        return "Parâmetro secretary inválido."

    if crime and crime not in VALID_CRIMES_DF and crime not in VALID_CRIMES_SP:
        return "Parâmetro crime inválido."

    if initial_month and final_month:
        if not validate_period(initial_period=initial_month, final_period=final_month):
            return "Parâmetros initial_month/final_month inválidos."
    elif (initial_month and final_month is None) or (final_month and initial_month is None):
        return "Parâmetros initial_month e final_month devem ser passados juntos."

    if per_capita and (per_capita != '1' and per_capita != '0'):
        return "Parâmetro per_capita inválido."

    return None

def validate_period(initial_period, final_period):
    initial_period = initial_period.split('/')
    initial_month = int(initial_period[0])
    initial_year = int(initial_period[1])

    final_period = final_period.split('/')
    final_month = int(final_period[0])
    final_year = int(final_period[1])

    date = datetime.datetime.now()
    current_year = date.year
    
    if initial_month not in range(1, 13) or final_month not in range(1, 13):
        return False

    if initial_year not in range(2018, current_year+1) \
            or final_year not in range(2018, current_year+1):
        return False

    if initial_month > final_month and initial_year == final_year \
            or initial_year > final_year:
        return False

    return True
