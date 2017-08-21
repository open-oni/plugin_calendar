import calendar

from django import forms
from django.core import urlresolvers
from django.db import connection
from django.db.models import Count

from core import models

class Day(object):
    def __init__(self, week, daydata):
        self.week = week
        self.day_of_month = daydata[0]
        self.day_of_week = daydata[1]
        self.month = self.week.month.num
        self.year = self.week.month.cal.year
        self.dtstr = "%04d%02d%02d" % (self.year, self.month, self.day_of_month)
        self.issue_count = 0

        if self.dtstr in self.week.month.cal.date_counts:
            self.issue_count = self.week.month.cal.date_counts[self.dtstr]

        if self.issue_count is None:
            self.issue_count = 0

    def link(self):
        lccn = "all"
        if self.week.month.cal.title is not None:
            lccn = self.week.month.cal.title.lccn

        return urlresolvers.reverse('calendar_issues_for_date', kwargs=dict(
            lccn = lccn,
            year = "%04d" % self.year,
            month = "%02d" % self.month,
            day = "%02d" % self.day_of_month,
        ))

class Week(object):
    def __init__(self, month, weekdata):
        self.month = month
        self.weekdata = weekdata
        self._setup_days()

    def _setup_days(self):
        self.days = []
        for daydata in self.weekdata:
            self.days.append(Day(self, daydata))

class Month(object):
    def __init__(self, cal, num):
        self.cal = cal
        self.num = num
        self._setup_weeks()

    def name(self):
        return calendar.month_name[self.num]

    def _setup_weeks(self):
        self.weeks = []
        raw_weeks = self.cal.monthdays2calendar(self.cal.year, self.num)

        for weekdata in raw_weeks:
            self.weeks.append(Week(self, weekdata))

class IssueCalendar(calendar.Calendar):
    def __init__(self, title, year):
        calendar.Calendar.__init__(self, 6)
        self.title = title
        self.year = year
        self._get_issue_years()
        self._normalize_selected_year()
        self._get_issue_dates_for_selected_year()
        self._setup_months()

    def _get_issue_years(self):
        """Set up an array of years and issue counts for each year"""
        cursor = connection.cursor()
        select = "SELECT year(date_issued) AS issue_year, COUNT(id) FROM core_issue"
        where = ""
        params = []
        if self.title is not None:
            where = "WHERE title_id = %s"
            params = [self.title.lccn]
        grouporder = "GROUP BY issue_year ORDER BY issue_year"
        cursor.execute("%s %s %s" % (select, where, grouporder), params)
        self.yeardata = cursor.fetchall()

    def _normalize_selected_year(self):
        """Determine the selected year in case one was not already selected"""
        if len(self.yeardata) > 0:
            if self.year is None:
                self.year = self.yeardata[0][0]
            else:
                self.year = int(self.year)
        else:
            self.year = 1900

    def _get_issue_dates_for_selected_year(self):
        """Get a count of issues for each day of the selected year"""
        self.date_counts = {}
        qs = models.Issue.objects.filter(date_issued__year = self.year)
        if self.title is not None:
            qs = qs.filter(title_id = self.title.lccn)
        qs = qs.annotate(num_issues = Count("date_issued", distinct = True))
        for issue in qs.all():
            dtstr = "%04d%02d%02d" % (issue.date_issued.year, issue.date_issued.month, issue.date_issued.day)
            self.date_counts[dtstr] = issue.num_issues

    def _setup_months(self):
        self.months = []
        for m in range(12):
            self.months.append(Month(self, m+1))

    def year_form(self):
        class SelectYearForm(forms.Form):
            year = forms.fields.ChoiceField(
                choices=((yd[0], "%d (%d)" % (yd[0], yd[1])) for yd in self.yeardata),
                initial=self.year
            )

        return SelectYearForm()
