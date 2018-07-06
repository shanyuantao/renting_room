"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 1.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'gj-i26l&ka(np^6j@!0jqa0sr-s)eb@h7ux0to##!xgs53r+j!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True  # DEBUG等于false等于自己去处理遇到的错误, 且不会处理静态文件

ALLOWED_HOSTS = ['*'] # 允许所有主机


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
<<<<<<< HEAD
    'detail'
=======
    'cwdapp'
>>>>>>> cwd
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'room',
        'USER': 'root',
        'PASSWORD': '2905058',
        'PORT': '3306',
        'HOST': '101.132.39.189'
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

# 配置静态文件
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
# STATIC_ROOT = STATICFILES_DIRS[0]  # 同上

# 配置上传文件路径
MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 没有登录的跳转地址
# LOGIN_URL = ''

# 创建日志路径
LOG_PATH = os.path.join(BASE_DIR, 'log')

# 如果地址不存在, 则自动创建log文件夹
if not os.path.isdir(LOG_PATH):
    os.mkdir(LOG_PATH)

LOGGING = {
    'version': 1,
    'disable_exisiting_loggers':False,
    'formatters': {
        'default': {
            'format': '%(levelname)s %(funcName)s %(asctime)s %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(created)s %(message)s'
        }
    },

    'handlers': {
        'stu_handlers': {
            'level': 'DEBUG',
            # 日志文件指定为5M, 超过5M重新备份, 然后写入新的日志文件
            'class': 'logging.handlers.RotatingFileHandler',
            # 1M=1024Kb 1Kb = 1024b
            'maxBytes': 5 * 1024 * 1024,
            # 文件地址
            'filename': '%s/log.txt' % LOG_PATH,
            'formatter': 'default',
        },
        'uauth_handlers': {
            'level': 'DEBUG',
            # 日志文件指定为5M, 超过5M重新备份, 然后写入新的日志文件
            'class': 'logging.handlers.RotatingFileHandler',
            # 1M=1024Kb 1Kb = 1024b
            'maxBytes': 5 * 1024 * 1024,
            # 文件地址
            'filename': '%s/uauth_log.txt' % LOG_PATH,
            'formatter': 'simple',
        }
    },
    'loggers': {
        'stu': {
            'handlers': ['stu_handlers'],
            'level': 'INFO'
        },
        'auth': {
            'handlers': ['uauth_handlers'],
            'level': 'INFO'
        }
    },
    'filters': {

    }
}
