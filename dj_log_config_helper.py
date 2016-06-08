# -*- coding: utf-8 -*-

import os
import logging.config
import logging

from django.conf import settings

DEFAULT_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s\t%(asctime)s.%(msecs)03dZ\t%(name)s:%(lineno)s\t%(message)s',
            'datefmt': '%Y-%m-%dT%H:%M:%S'
        },
        'simple': {
            'format': '%(levelname)s\t%(name)s:%(lineno)s\t%(message)s',
        }
    },
    'handlers': {
        # By default, log to console
        'default': {
            'level': logging.DEBUG,
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        }
    },
    # This is the default logger for any apps or libraries that use the logger
    # package, but are not represented in the `loggers` dict below.  A level
    # must be set and handlers defined.  Setting this logger is equivalent to
    # setting and empty string logger in the loggers dict below, but the separation
    # here is a bit more explicit.  See link for more details:
    # https://docs.python.org/2.7/library/logging.config.html#dictionary-schema-details
    'root': {
        'level': logging.WARNING,
        'handlers': ['default'],
    },
}


def _sanitize_app_loggers(apps_list):
    sanitized_apps = {app.split('.')[0] for app in apps_list}
    return sanitized_apps


def _configure_logging(log_settings, log_level, apps=None):

    if apps is None:
        apps = _sanitize_app_loggers(settings.INSTALLED_APPS)

    app_loggers = {}
    for app in apps:
        app_loggers[app] = {
            'level': log_level,
            'handlers': ['default'],
            'propogate': False,
        }

    log_settings['loggers'] = app_loggers

    logging.config.dictConfig(log_settings)


def configure_file_logging(log_level, log_file_root, apps=None):
    log_filename = 'django-{}.log'.format(os.path.basename(settings.BASE_PATH))

    logger = dict(DEFAULT_LOGGING)
    # Update the default handler to be a watched file handler
    logger['default'] = {
        'class': 'logging.handlers.WatchedFileHandler',
        'level': log_level,
        'formatter': 'verbose',
        'filename': os.path.join(log_file_root, log_filename),
    }

    _configure_logging(logger, log_level, apps)


def configure_console_logging(log_level, apps=None):
    _configure_logging(dict(DEFAULT_LOGGING), log_level, apps)
