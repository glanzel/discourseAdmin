
Skip to content
Pull requests
Issues
Marketplace
Explore
@glanzel
glanzel /
discourseAdmin

2
0

    0

Code
Issues
Pull requests
Actions
Projects
Wiki
Security
Insights

    Settings

discourseAdmin/dsso/settings_local.py.template
grischan testing
Latest commit 210d088 10 hours ago
History
1 contributor
94 lines (80 sloc) 2.45 KB
import os

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'a_really_seceret_key'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DOMAIN_NAME= 'localhost'
IS_DEV = True
IS_PROD = False

ALLOWED_HOSTS = []

DISCOURSE_API_HOST = 'http://localhost:3000'
DISCOURSE_API_USERNAME = 'system'
DISCOURSE_API_KEY = 'a_secret_key'

DISCOURSE_SSO_KEY = 'test-abcd'
DISCOURSE_BASE_URL = 'http://localhost:3000'
#DISCOURSE_INTERN_SSO_EMAIL = 'bekanntedomain.de'

PHP_LOGIN_CHECK_URI = None
PHP_LOGIN_CHECK_AUTH = None
#DEACTIVATE_INACTIVE_AFTER_DAYS = 365 #uncomment get automatic called at logout or call url/deactivate_inactive per cronjob  Zeit in Tagen

INTERNAL_IPS = [
    'localhost'
    '127.0.0.1',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mydatabase',
    }
}

LOG_DIR = "."
# RECOMENDED: choose another log diretory, but make sure that your dir existis bevor
#LOG_DIR = "/var/log/discoursAdmin"


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default':{
            'format': '{levelname} {asctime} {module}:{lineno} {message}',
            'style': '{',
        },
        'simple':{
            'format': '{levelname} {message}',
            'style': '{',
        },
        'time':{
            'format': '{asctime} {message}',
            'style': '{',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        },
        'file': {
            'class':'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR + "/dsso.log",        
            'formatter': 'default'
        },
        'deactivate_inactive':{
            'formatter': 'time',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR + "/deactivate_inactive.log",        
        }
    },
    'loggers':{
        '': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'views.deactivate_inactive':{
            'handlers':['deactivate_inactive'],
            'level': 'INFO',
            'propagate': False,
        }
    },

}
