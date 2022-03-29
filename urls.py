from django.urls import include, path, re_path
from onisite.plugins.calendar import views

urlpatterns = [
    # Override core's /issues, which is the calendar for the first year that
    # has any content ingested
    re_path(r'^issues/$', views.all_issues_calendar, name="calendar_all_issues_calendar"),

    # Override core's calendar for a user-specified year
    re_path(r'^issues/(?P<year>\d{4})$', views.all_issues_calendar, name="calendar_all_issues_calendar_for_year"),

    # Override core's title-specific calendar for the first year available
    re_path(r'^lccn/(?P<lccn>\w+)/issues/$', views.title_issues_calendar, name="calendar_title_issues_calendar"),

    # Override core's title-specific calendar for a user-specified year
    re_path(r'^lccn/(?P<lccn>\w+)/issues/(?P<year>\d{4})$',
       views.title_issues_calendar, name="calendar_title_issues_calendar_for_year"),

    # New handler: issue list for a given date
    re_path(r'^issues/(?P<lccn>\w+)/(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})/$',
        views.issues_for_date, name="calendar_issues_for_date"),
]
