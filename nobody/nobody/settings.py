# -*- coding:utf-8 -*-

import os
from datetime import timedelta

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


ALLOWED_HOSTS = ['*']

LANGUAGE_CODE = 'zh-cn'
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True
USE_L10N = True
USE_TZ = False

DATE_FORMAT = 'Y-m-d'
DATETIME_FORMAT = '%s H:i:s' % DATE_FORMAT

DATE_INPUT_FORMATS = ('%Y-%m-%d',)
DATETIME_INPUT_FORMATS = ('%Y-%m-%d %H:%M:%S',)


# Django setting
DEBUG = True
TEMPLATE_DEBUG = DEBUG
SQL_DEBUG = False

SECRET_KEY = '+cw4%1d8^nq*r6+o0nj9wh&vrd^-3jd722t7(yiri3+oq#_la+'

# Application definition

INSTALLED_APPS = (
    # 查找模板和静态文件时，列在前面的 app 有更高的优先级
    # nobody related apps
    'nobody',

    'magnet',
    'captcha',
    'proxy',

    'people',

    # Third party apps
    'ajaxuploader',
    'floppyforms',
    'mptt',

    'rest_framework',

    # Django internal apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# TODO What's this...
TEMPlATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

ROOT_URLCONF = 'nobody.urls'
WSGI_APPLICATION = 'nobody.wsgi.application'

# AUTH_USER_MODEL = 'audit.User'
# TEST_RUNNER = 'test_runner.BladeRunner'

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]
# FIXTURE_DIRS = ('/banker/fixtures/', )

STATIC_BASE = os.path.join(BASE_DIR, 'static')
STATIC_ROOT = os.path.join(STATIC_BASE, 'tmp')
STATIC_DIST = os.path.join(STATIC_BASE, 'dist')

STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'nobody',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '127.0.0.1',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': 'localhost:6379',
        'OPTIONS': {
            'DB': 1,
            'PASSWORD': '',
            'PARSER_CLASS': 'redis.connection.HiredisParser',
            'CONNECTION_POOL_CLASS': 'redis.BlockingConnectionPool',
            'CONNECTION_POOL_CLASS_KWARGS': {
                'max_connections': 50,
                'timeout': 20,
                'socket_timeout': 0.5,
                'retry_on_timeout': True,
            }
        }
    }
}

# LOGGING
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    # 格式器
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },

    'filters': {

    },

    'handlers': {
        # Null处理器，所有高于（包括）debug的消息会被传到/dev/null
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },

        # 流处理器，所有的高于（包括）debug的消息会被传到stderr，使用的是simple格式器
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },

        # AdminEmail处理器，所有高于（包括）而error的消息会被发送给站点管理员，使用的是special格式器
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },

    'loggers': {
        # 使用null处理器，所有高于（包括）info的消息会被发往null处理器，向父层次传递信息
        'django.security': {
            'handlers': ['null'],
            'level': 'INFO',
        },

        # 所有高于（包括）error的消息会被发往mail_admins处理器，消息不向父层次发送
        'django.request': {
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO',
            # 'propagate': False,  TODO what's propagate?
        },

        # 所有高于（包括）info的消息同时会被发往console和mail_admins处理器，使用special过滤器
        'nobody': {
            # 'handlers': ['console', 'mail_admins'],
            'handlers': ['console'],
            'level': 'INFO',
        }
    }
}

# REDIS CONF
REDIS_CONF = {
    'host': 'localhost',
    'port': 6379,
    'db': 2
}

# CELERY CONF
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_BROKER_URL = 'redis://localhost:6379/0'

REQUESTS_LOG_PATH = '.'
