import calendar

class IssueCalendar(calendar.Calendar):
    """
    This calendar returns complete HTML pages.
    """

    def __init__(self, firstweekday=0, issues=None, all_issues=False):
        calendar.Calendar.__init__(self, firstweekday)
        self.issues = issues
        self.all_issues = all_issues

    # CSS classes for the day <td>s
    cssclasses = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]

    def formatday(self, year, month, day, weekday):
        """
        Return a day as a table cell.
        """
        if day == 0:
            return '<td class="noday">&nbsp;</td>'  # day outside month
        else:
            r = self.issues.filter(date_issued=datetime.date(year, month, day))
            issues = set()
            for issue in r:
                issues.add((issue.title.lccn,
                            issue.date_issued, 
                            issue.edition,
                            issue.title
                            ))
            issues = sorted(list(issues))
            count = len(issues)
            if count == 1:
                _class = "single"
                lccn, date_issued, edition, title = issues[0]
                kw = dict(lccn=lccn, date=date_issued, edition=edition)
                url = urlresolvers.reverse('openoni_issue_pages', kwargs=kw)
                if self.all_issues:
                    # list the title(s) being linked since this view is for all papers
                    _day = """<div class='btn-group'><a class='btn dropdown-toggle' 
                        data-toggle='dropdown' href='#'>
                        """
                    _day += """%s<span class='caret'></span></a>""" % day
                    _day += "<ul class='dropdown-menu'>"
                    _day += """<li><a href="%s">%s</a></li>""" % (url, title)
                    _day += "</ul></div>"
                else:
                    # if specific paper, 
                    _day = """<a href="%s">%s</a>""" % (url, day)
            elif count > 1:
                _class = "multiple"
                # use a dropdown instead of expanding the calendar to display multiple titles
                _day = """<div class='btn-group'><a class='btn dropdown-toggle' 
                    data-toggle='dropdown' href='#'>
                    """
                _day += """%s<span class='caret'></span></a>""" % day
                _day += "<ul class='dropdown-menu'>"
                for lccn, date_issued, edition, title in issues:
                    kw = dict(lccn=lccn, date=date_issued, edition=edition)
                    url = urlresolvers.reverse('openoni_issue_pages',
                                               kwargs=kw)
                    if self.all_issues:
                        _day += """<li><a href="%s">%s</a></li>""" % (url, title)
                    else:
                        _day += """<li><a href="%s">ed-%d</a></li>""" % (url, edition)
                _day += "</ul></div>"
            else:
                _class = "noissues"
                _day = day
            return '<td class="%s %s">%s</td>' % (_class,
                                                  self.cssclasses[weekday],
                                                  _day)

    def formatweek(self, year, month, theweek):
        """
        Return a complete week as a table row.
        """
        s = ''.join(self.formatday(year, month, d, wd) for (d, wd) in theweek)
        return '<tr>%s</tr>' % s

    def formatweekday(self, day):
        """
        Return a weekday name as a table header.
        """
        return '<td class="dayname %s">%s</td>' % (self.cssclasses[day],
                                                   calendar.day_abbr[day][0])

    def formatweekheader(self):
        """
        Return a header for a week as a table row.
        """
        s = ''.join(self.formatweekday(i) for i in self.iterweekdays())
        return '<tr class="daynames">%s</tr>' % s

    def formatmonthname(self, theyear, themonth, withyear=True):
        """
        Return a month name as a table row.
        """
        if withyear:
            s = '%s %s' % (calendar.month_name[themonth], theyear)
        else:
            s = '%s' % calendar.month_name[themonth]
        return '<tr><td colspan="7" class="title">%s, %s</td></tr>' % (s,
                                                                       theyear)

    def formatmonth(self, theyear, themonth, withyear=True):
        """
        Return a formatted month as a table.
        """
        v = []
        a = v.append
        a('<table border="0" cellpadding="0" cellspacing="0" class="month table table-condensed table-bordered">')
        a('\n')
        a(self.formatmonthname(theyear, themonth, withyear=withyear))
        a('\n')
        a(self.formatweekheader())
        a('\n')
        weeks = self.monthdays2calendar(theyear, themonth)
        while len(weeks) < 6:
            # add blank weeks so all calendars are 6 weeks long.
            weeks.append([(0, 0)] * 7)
        for week in weeks:
            a(self.formatweek(theyear, themonth, week))
            a('\n')
        a('</table>')
        a('\n')
        return ''.join(v)

    def formatyear(self, theyear, width=4):
        """
        Return a formatted year as a div of tables.
        """
        v = []
        a = v.append
        width = max(width, 1)
        a('<div cellspacing="0" class="calendar_wrapper">')
        for i in range(calendar.January, calendar.January + 12, width):
            # months in this row
            months = range(i, min(i + width, 13))
            a('<div class="calendar_row">')
            for m in months:
                a('<div class="span3 calendar_month">')
                a(self.formatmonth(theyear, m, withyear=False))
                a('</div>')
            a('</div>')
        a('</div>')
        return ''.join(v)
