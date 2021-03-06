"""Settings for production"""
import os

import raven

from . import *

DEBUG = False

ALLOWED_HOSTS = ["161.35.94.31", "pur-beurre-mbi.site", "www.pur-beurre-mbi.site"]

INSTALLED_APPS += [
    "raven.contrib.django.raven_compat",
]


RAVEN_CONFIG = {
    "dsn": "https://f48177d43ab0454bbe2e494e77f5def1@o466057.ingest.sentry.io/5479819",
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    "release": raven.fetch_git_sha(os.path.dirname(os.pardir)),
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "root": {
        "level": "INFO",  # WARNING by default. Change this to capture more than warnings.
        "handlers": ["sentry"],
    },
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s "
            "%(process)d %(thread)d %(message)s"
        },
    },
    "handlers": {
        "sentry": {
            "level": "INFO",  # To capture more than ERROR, change to WARNING, INFO, etc.
            "class": "raven.contrib.django.raven_compat.handlers.SentryHandler",
            "tags": {"custom-tag": "x"},
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django.db.backends": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": False,
        },
        "raven": {
            "level": "DEBUG",
            "handlers": ["console"],
            "propagate": False,
        },
        "sentry.errors": {
            "level": "DEBUG",
            "handlers": ["console"],
            "propagate": False,
        },
    },
}

# SECURITY
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
