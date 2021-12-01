from django.utils import timezone as tz


def year(request):
    cur_year = tz.now().year
    return {
        'year': cur_year
    }
