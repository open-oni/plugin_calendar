from django.conf.urls import url, include
from onisite.plugins.calendar import views

urlpatterns = [
    # Override core's /issues, which is the calendar for the first year that
    # has any content ingested.  Note that the final slash is optional since we
    # may one day make all the core URLs more consistent.
    url(r'^issues/?$', views.issues, name="calendar_issues"),

    # Override core's calendar for a user-specified year
    url(r'^issues/(?P<year>\d{4})/?$', views.issues, name="calendar_issues_for_year"),

    # Override core's title-specific calendar for the first year available
    url(r'^lccn/(?P<lccn>\w+)/issues/?$', views.issues_title, name="calendar_issues_title"),

    # Override core's title-specific calendar for a user-specified year
    url(r'^lccn/(?P<lccn>\w+)/issues/(?P<year>\d{4})/?$',
       views.issues_title, name="calendar_issues_title_for_year"),
]
