from django import forms
from django.conf import settings
from core import models
from core.decorator import cache_page
from django.shortcuts import get_object_or_404, render

@cache_page(settings.DEFAULT_TTL_SECONDS)
def all_issues_calendar(request, year=None):
    issues = models.Issue.objects.all().order_by('date_issued')
    page_title = "Browse All Issues"
    page_name = "issues"
    crumbs = list(settings.BASE_CRUMBS)
    select_year_form = _issues_year_select(issues, year)
    return render(request, 'all_issues_calendar.html', locals())

@cache_page(settings.DEFAULT_TTL_SECONDS)
def title_issues_calendar(request, lccn, year=None):
    title = get_object_or_404(models.Title, lccn=lccn)
    issues = title.issues.all()
    page_title = "Browse Issues: %s" % title.display_name
    page_name = "issues_title"
    crumbs = create_crumbs(title)
    select_year_form = _issues_year_select(issues, year)
    return render(request, 'title_issues_calendar.html', locals())

def _issues_year_select(issues, start_year):
    if issues.count() > 0:
        if start_year is None:
            start_year = issues[0].date_issued.year
        else:
            start_year = int(start_year)
    else:
        start_year = 1900
    dates = issues.dates('date_issued', 'year')

    class SelectYearForm(forms.Form):
        year = forms.fields.ChoiceField(choices=((d.year, d.year) for d in dates), initial=start_year)

    return SelectYearForm()
