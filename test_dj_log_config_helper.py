# -*- coding: utf-8 -*-
# !/usr/bin/env python

import unittest
import logging
import tempfile

import django
from django.conf import settings
from django.test import SimpleTestCase, override_settings
from django.core.exceptions import ImproperlyConfigured

import dj_log_config_helper as log_helper


class LogHelperTestSuite(SimpleTestCase):
    """Basic test cases."""

    def test_app_modules_are_normalized(self):
        app_modules = [
            'django.contrib.auth',
            'django.contrib.sessions',
            'django.contrib.messages'
        ]
        apps = log_helper._normalize_apps(app_modules)

        self.assertEqual(len(apps), 1)
        self.assertIn('django', apps)

    def test_app_loggers_empty_when_no_apps(self):
        loggers = log_helper.build_app_loggers(
            logging.DEBUG,
            []
        )
        self.assertFalse(loggers)

    def test_app_loggers_built_with_default_handler(self):
        level = logging.INFO
        apps = ['django.contrib.auth', 'myapp']
        loggers = log_helper.build_app_loggers(level, apps)

        self.assertTrue(loggers)
        for key, value in loggers.iteritems():
            self.assertIn(key, loggers)
            self.assertEqual(value['level'], level)
            self.assertEqual(value['propagate'], False)
            self.assertEqual(value['handlers'], ['default'])

    def test_app_loggers_built_with_custom_handler(self):
        level = logging.INFO
        apps = ['django']
        handlers = ['handler1', 'handler2']
        loggers = log_helper.build_app_loggers(level, apps, handlers)

        self.assertEqual(loggers['django']['handlers'], handlers)

    def test_app_loggers_built_with_string_handler(self):
        level = logging.INFO
        apps = ['django']
        str_handler = 'myhandler'
        loggers = log_helper.build_app_loggers(
            level, apps, str_handler)

        self.assertEqual(loggers['django']['handlers'], list(str_handler))

    def test_build_config_defaults(self):
        level = logging.WARNING
        verbose = False
        apps = ['django.contrib.auth']
        config = log_helper._build_logging_config(
            level, apps, verbose)

        self.assertEqual(config['handlers']['default']['class'], 'logging.StreamHandler')
        self.assertEqual(config['handlers']['default']['level'], logging.DEBUG)
        self.assertEqual(config['handlers']['default']['formatter'], 'simple')

    def test_build_config_file_handler(self):
        level = logging.WARNING
        verbose = False
        apps = ['django.contrib.auth']
        # Must be a path that is writable
        tf = tempfile.NamedTemporaryFile()
        config = log_helper._build_logging_config(
            level, apps, verbose, filename=tf.name)

        self.assertEqual(
            config['handlers']['default']['class'],
            'logging.handlers.WatchedFileHandler')
        self.assertEqual(
            config['handlers']['default']['filename'], tf.name)

    def test_build_log_config_app_loggers(self):
        level = logging.WARNING
        verbose = False
        apps = [
            'django.contrib.auth',
            'django.contrib.sessions',
            'django.contrib.messages'
        ]
        config = log_helper._build_logging_config(
            level, apps, verbose)

        loggers = config['loggers']
        self.assertTrue(len(loggers), 3)
        self.assertEqual(loggers['django.contrib.auth']['level'], level)
        self.assertEqual(loggers['django.contrib.auth']['handlers'], ['default'])
        self.assertEqual(loggers['django.contrib.auth']['propagate'], False)

    def test_build_log_config_verbose_mode(self):
        level = logging.WARNING
        verbose = True
        apps = [
            'django.contrib.auth',
            'django.contrib.sessions',
            'django.contrib.messages'
        ]
        config = log_helper._build_logging_config(
            level, apps, verbose)

        self.assertEqual(
            config['handlers']['default']['formatter'], 'verbose')

    def test_configure_logger_with_default_settings_raises_improperly_configured(self):
        """By default, the LOGGING_CONFIG setting is enabled in Django, but for this
        module to work it needs to have been set to 'None' before calling."""
        with self.assertRaises(ImproperlyConfigured):
            log_helper.configure_installed_apps_logger(logging.DEBUG)

    @override_settings(LOGGING_CONFIG=None)
    def test_configured_installed_apps_logger_defaults(self):
        """Test out the configuration of the 'django' logger when LOGGING_CONFIG is set
        to None.  The configuration is expected to be done in a project's
        settings file, so to simulate that we need to first configure the logger
        and then call django.setup(), which is normally called when running a
        management command or running a WSGI server - see
        https://docs.djangoproject.com/en/1.9/ref/applications/#how-applications-are-loaded.
        """

        log_helper.configure_installed_apps_logger(logging.INFO)

        # Need to set up the application registry in order to access
        # installed_apps
        django.setup()

        # A logger should have been set up for "django" package with the default
        # handler, and given level and propagation
        dj_logger = logging.getLogger('django')
        self.assertEqual(len(dj_logger.handlers), 1)
        self.assertIsInstance(dj_logger.handlers[0], logging.StreamHandler)
        self.assertEqual(dj_logger.handlers[0].name, 'default')
        self.assertEqual(dj_logger.level, logging.INFO)
        self.assertEqual(dj_logger.propagate, False)

    @override_settings(LOGGING_CONFIG=None)
    def test_configured_installed_apps_logger_with_added_packages_list(self):
        """Test out the configuration of an additional package logger. """

        pkgs = ['rq.worker']

        log_helper.configure_installed_apps_logger(logging.INFO,
                                                   additional_packages=pkgs)

        # Need to set up the application registry in order to access
        # installed_apps
        django.setup()

        # A logger should have been set up for the additional app package with
        # the default handler, and given level and propagation
        additional_logger = logging.getLogger(pkgs[0])
        self.assertEqual(len(additional_logger.handlers), 1)
        self.assertIsInstance(additional_logger.handlers[0],
                              logging.StreamHandler)
        self.assertEqual(additional_logger.handlers[0].name, 'default')
        self.assertEqual(additional_logger.level, logging.INFO)
        self.assertEqual(additional_logger.propagate, False)

    @override_settings(LOGGING_CONFIG=None)
    def test_configured_installed_apps_logger_with_added_packages_string(self):
        """Test out the configuration of an additional package logger passed in as
        a string instead of a list.
        """

        pkg = 'rq.worker'

        log_helper.configure_installed_apps_logger(logging.INFO,
                                                   additional_packages=pkg)

        # Need to set up the application registry in order to access
        # installed_apps
        django.setup()

        # A logger should have been set up for the additional app package with
        # the default handler, and given level and propagation
        additional_logger = logging.getLogger(pkg)
        self.assertEqual(len(additional_logger.handlers), 1)
        self.assertIsInstance(additional_logger.handlers[0],
                              logging.StreamHandler)
        self.assertEqual(additional_logger.handlers[0].name, 'default')
        self.assertEqual(additional_logger.level, logging.INFO)
        self.assertEqual(additional_logger.propagate, False)


if __name__ == '__main__':
    # Test without a settings file by calling settings.configure
    # See: https://docs.djangoproject.com/en/1.9/topics/settings/#using-settings-without-setting-django-settings-module
    settings.configure(
        INSTALLED_APPS=['django.contrib.auth', 'django.contrib.contenttypes']
    )
    unittest.main()
