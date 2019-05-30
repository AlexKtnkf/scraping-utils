from datetime import datetime as dt
from datetime import timedelta as td
import pytz


# fonction de sérialisation de datetime
# retourne un dictionnaire d'informations sur la date passée en input
# si la date passée est de type string, préciser le format utilisé
# exemple : serialize_date('20/01/2019', str_format='%d/%m/%Y')
# si la date passée vient d'un autre fuseau horaire et doit être convertie,
# indiquer le décalage sous forme d'entier (positif ou négatif) en second paramètre
# exemple : serialize_date(dt.now(), correct_tz=+2)
def serialize_date(raw_date, correct_tz=None, str_format=None):
    passed_date = raw_date
    local = pytz.timezone('Europe/Paris')
    if isinstance(raw_date, int):
        passed_date = dt.fromtimestamp(raw_date)
    if isinstance(raw_date, str):
        passed_date = dt.fromtimestamp(dt.strptime(raw_date.strip(), str_format).timestamp())
    if correct_tz is not None:
        passed_date = passed_date + td(hours=correct_tz)
    if passed_date.tzinfo is None:
        naive_date = passed_date
        passed_date = local.localize(passed_date)
    else:
        naive_date = passed_date.replace(tzinfo=None)
    string_date = passed_date.strftime("%d-%m-%Y %H:%M:%S%z")
    date_infos = {
        'raw': raw_date,
        'iso': passed_date.isoformat(),
        'timestamp': passed_date.timestamp(),
        'date': string_date.split(' ')[0],
        'time': string_date.split(' ')[1].split('+')[0],
        'year': passed_date.year,
        'month': passed_date.month,
        'day': passed_date.day,
        'day_of_week': passed_date.strftime('%A'),
        'rounded': round_time(naive_date, round_to=60 * 10).isoformat(),
        'log': dt.now().isoformat(),
        'string': string_date
    }
    return date_infos


# fonction pour arrondir l'heure
def round_time(passed_dt=None, round_to=60):
    if passed_dt == None:
        passed_dt = dt.now()
    seconds = (passed_dt - passed_dt.min).seconds
    rounding = (seconds + round_to / 2) // round_to * round_to
    return passed_dt + td(0, rounding - seconds, -passed_dt.microsecond)


