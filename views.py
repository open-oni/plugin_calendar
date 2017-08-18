from django.conf import settings
from core import models
from core.decorator import cache_page
from django.shortcuts import get_object_or_404, render

@cache_page(settings.DEFAULT_TTL_SECONDS)
def issues(request, year=None):
    issues = models.Issue.objects.all().order_by('date_issued')
    page_title = "Browse All Issues"
    page_name = "issues"
    crumbs = list(settings.BASE_CRUMBS)
    return render(request, 'issues_calendar.html', locals())

@cache_page(settings.DEFAULT_TTL_SECONDS)
def issues_title(request, lccn, year=None):
    title = get_object_or_404(models.Title, lccn=lccn)
    issues = title.issues.all()
    page_title = "Browse Issues: %s" % title.display_name
    page_name = "issues_title"
    crumbs = create_crumbs(title)
    return render(request, 'issues_title_calendar.html', locals())
