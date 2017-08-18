from django.conf.urls import url, include
from onisite.plugins.calendar import views

urlpatterns = [
    # Override core's /issues, which is the calendar for the first year that
    # has any content ingested
    url(r'^issues/$', views.all_issues_calendar, name="calendar_all_issues_calendar"),

    # Override core's calendar for a user-specified year
    url(r'^issues/(?P<year>\d{4})$', views.all_issues_calendar, name="calendar_all_issues_calendar_for_year"),

    # Override core's title-specific calendar for the first year available
    url(r'^lccn/(?P<lccn>\w+)/issues/$', views.title_issues_calendar, name="calendar_title_issues_calendar"),

    # Override core's title-specific calendar for a user-specified year
    url(r'^lccn/(?P<lccn>\w+)/issues/(?P<year>\d{4})$',
       views.title_issues_calendar, name="calendar_title_issues_calendar_for_year"),
]
