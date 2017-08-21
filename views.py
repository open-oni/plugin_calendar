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
