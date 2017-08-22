import calendar
import datetime

from django.conf import settings
from django.shortcuts import get_object_or_404, render

from core import models
from core.decorator import cache_page
from core.utils.utils import create_crumbs

from issue_calendar import IssueCalendar

@cache_page(settings.DEFAULT_TTL_SECONDS)
def all_issues_calendar(request, year=None):
    page_title = "Browse All Issues"
    page_name = "issues"
    crumbs = list(settings.BASE_CRUMBS)
    calendar = IssueCalendar(None, year)
    return render(request, 'all_issues_calendar.html', locals())

@cache_page(settings.DEFAULT_TTL_SECONDS)
def title_issues_calendar(request, lccn, year=None):
    title = get_object_or_404(models.Title, lccn=lccn)
    page_title = "Browse Issues: %s" % title.display_name
    page_name = "issues_title"
    crumbs = create_crumbs(title)
    calendar = IssueCalendar(title, year)
    return render(request, 'title_issues_calendar.html', locals())

@cache_page(settings.DEFAULT_TTL_SECONDS)
def issues_for_date(request, lccn, year, month, day):
    m, d, y = int(month), int(day), int(year)
    page_title = "Issues published on %s %d, %d" % (calendar.month_name[m], d, y)
    dt = datetime.date(y, m, d)
    page_name = "issues_for_date"

    if lccn == "all":
        issues = models.Issue.objects.filter(date_issued = dt)

    else:
        title = get_object_or_404(models.Title, lccn=lccn)
        issues = models.Issue.objects.filter(date_issued = dt, title_id = lccn)
        if len(issues) > 1:
            page_title = title.name + ": " + page_title
        else:
            # TODO: Redirect!
            page_title="Redirect me!"

    dtstr = "%04d-%02d-%02d" % (y, m, d)
    return render(request, 'issues_for_date.html', locals())
