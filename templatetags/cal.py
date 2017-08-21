import calendar
from django import template

register = template.Library()

@register.inclusion_tag('year_calendar.html')
def year_calendar(cal):
    return {
        'month_rows': [
            (cal.months[0], cal.months[1], cal.months[2], cal.months[3]),
            (cal.months[4], cal.months[5], cal.months[6], cal.months[7]),
            (cal.months[8], cal.months[9], cal.months[10], cal.months[11]),
        ],
        'calendar': cal,
    }

@register.simple_tag
def month_name(m):
    return calendar.month_name[m]
