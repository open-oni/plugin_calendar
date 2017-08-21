from django import forms
from django.db import connection
from django.conf import settings
from django.shortcuts import get_object_or_404, render

from core import models
from core.decorator import cache_page
from core.utils.utils import create_crumbs

@cache_page(settings.DEFAULT_TTL_SECONDS)
def all_issues_calendar(request, year=None):
    page_title = "Browse All Issues"
    page_name = "issues"
    crumbs = list(settings.BASE_CRUMBS)
    select_year_form = _issues_year_select(None, year)
    return render(request, 'all_issues_calendar.html', locals())

@cache_page(settings.DEFAULT_TTL_SECONDS)
def title_issues_calendar(request, lccn, year=None):
    title = get_object_or_404(models.Title, lccn=lccn)
    page_title = "Browse Issues: %s" % title.display_name
    page_name = "issues_title"
    crumbs = create_crumbs(title)
    select_year_form = _issues_year_select(title, year)
    return render(request, 'title_issues_calendar.html', locals())

def _issues_year_select(title, start_year):
    yeardata = _all_issue_years(title)
    if len(yeardata) > 0:
        if start_year is None:
            start_year = yeardata[0][0]
        else:
            start_year = int(start_year)
    else:
        start_year = 1900

    class SelectYearForm(forms.Form):
        year = forms.fields.ChoiceField(
            choices=((yd[0], "%d (%d)" % (yd[0], yd[1])) for yd in yeardata),
            initial=start_year
        )

    return SelectYearForm()

def _all_issue_years(title):
    cursor = connection.cursor()
    select = "SELECT year(date_issued) AS issue_year, COUNT(id) FROM core_issue"
    where = ""
    params = []
    if title is not None:
        where = "WHERE title_id = %s"
        params = [title.lccn]
    grouporder = "GROUP BY issue_year ORDER BY issue_year"
    cursor.execute("%s %s %s" % (select, where, grouporder), params)
    yeardata = cursor.fetchall()

    return yeardata
