# Improved Calendar Open ONI Plugin

This plugin overrides the built-in calendar with a more accessible set of URLs
and templates for finding content for a given date.

## Setup

Clone the repository into your site's plugins directory:

```
git clone git@github.com:open-oni/plugin_calendar.git onisite/plugins/calendar
```

Add it to your `INSTALLED_APPS` in `onisite/settings_local.py`.  It should be
above 'core' to ensure it overrides the defaults.

    INSTALLED_APPS = (
        'django.contrib.humanize',
        'django.contrib.staticfiles',

        'onisite.plugins.calendar',
        'themes.oregon',
        'core',
    )

Put in a new URL path into `onisite/urls.py` above the `core.urls` line.  You
can put this plugin at whatever URL you prefer, but to override the core URLs,
you would do this:

```
  # Override the core all-issues calendars:
  url(r'', include("onisite.plugins.calendar.urls")),

  # ...

  # make sure you include your calendar links above the core urls
  url('', include("core.urls")),
```

If you choose not to override the core URLs, you will have to change your theme
to point to the calendar URLs manually, which is not recommended.  Core
generates URLs for calendar pages in quite a few locations.

Copy `config_example.py` to `config.py`. You may configure whether multiple issues
on the same day will be identifiable on the calendar with multiple titles. Calendars
which only display a single title always note where multiple issues were published
on the same day.

By default, multiples are not distinguished on the calendar with all titles.

```
# Display where multiple issues occur each day for all issues
# (multiple issues always show up on calendars for a single title)
MULTIPLES_ALL_ISSUES = True
```
