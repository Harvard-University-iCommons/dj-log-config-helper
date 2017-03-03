====================
Dj-Log-Config-Helper
====================

Centralize management of simple log configuration across Django projects

The ``dj_log_config_helper.configure_installed_apps_logger`` method configures either a console or file logger with a list of all the top-level app module packages being installed in ``INSTALLED_APPS``.  Use this method in your ``settings.py`` file.

Meta
----

* Author: Jaime Bermudez
* Email:  jaime_bermudez@harvard.edu
* Maintainer: Harvard University Academic Technology
* Email: tlt-ops@g.harvard.edu
* Status: active development, stable, maintained


Installation
------------
Simply run the following from within a virtualenv::

    $ pip install git+https://github.com/Harvard-University-iCommons/dj-log-config-helper

Running the tests
-----------------
Via make::

    $ make test

Usage
-----
Import the log config function in ``settings.py``::

    from dj_log_config_helper import configure_installed_apps_logger

Disable Django's default logging::

    LOGGING_CONFIG = None

At the end of ``settings.py`` configure a simple console logger::

    configure_installed_apps_logger(logging.INFO)

Or, configure a verbose file logger::

    configure_installed_apps_logger(logging.INFO, verbose=True, filename='django-project.log')

You can also log additional packages that are not part of INSTALLED_APPS::

    configure_installed_apps_logger(logging.INFO, additional_packages=['py.warnings'])
