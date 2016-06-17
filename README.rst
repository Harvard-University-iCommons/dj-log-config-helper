====================
Dj-Log-Config-Helper
====================

Centralize management of simple log configuration across Django projects

The `dj_log_config_helper.configure_installed_apps_logger` method configures either a console or file logger with a list of all the top-level app module packages being installed in `INSTALLED_APPS`.  Use this method in your `settings.py` file.

Meta
----

* Author: Jaime Bermudez
* Email:  jaime_bermudez@harvard.edu
* Maintainer: Harvard University Academic Technology
* Email: tlt-ops@g.harvard.edu
* Status: active development, stable, maintained


Installation
------------
.. code-block:: bash

    $ pip install git+https://github.com/Harvard-University-iCommons/dj-log-config-helper

Running the tests
-----------------
After installing inside of a virtualenv run the following:
.. code-block:: bash
    $ make test

Quick start
------------
Within your project's `settings.py` file:
1.  import the log config function::
    from dj_log_config_helper import configure_installed_apps_logger
2.  Set `LOGGING_CONFIG = None`
3.  At the end of your settings file, configure logging::
    configure_installed_apps_logger(logging.INFO, verbose=True, filename='django-project.log')
