# Improved Calendar Open ONI Plugin

This plugin overrides the built-in calendar with a more accessible set of URLs
and templates for finding content for a given date.

## Compatibility

The "master" branch should not be considered stable.  Unlike the core Open ONI
repository, plugins don't warrant the extra overhead of having separate
development branches, release branches, etc.  Instead, it is best to find a tag
that works and stick with that tag.

- Calendar v0.3.0 and prior only work with Python 2 and Django 1.11 and prior
  - Therefore these versions of the Calendar plugin are only compatible up to
    (and including) ONI v0.11
- Calendar releases v0.4.0 and later require Python 3 and Django 2.2, and
  should be used with ONI 0.12 and later

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
