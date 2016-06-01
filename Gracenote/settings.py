# coding: utf-8
'''

Gracenote 設定ファイル

Created on 2016/03/23
Updated on 2016/03/23

@author: openkannyu
'''




####################################################################################################
# For Django's Setting
####################################################################################################
# Build paths
import os


BASE_DIR = os.path.dirname( os.path.dirname( __file__ ) )

# Secret key
SECRET_KEY = 'kx0-wc4vg)+s$y4q8gyo2w3vssds*b++o-=8p5ydqdeqo+#hox'


INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Gracenote',
 )
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
 )
ROOT_URLCONF = 'Gracenote.urls'
WSGI_APPLICATION = 'Gracenote.wsgi.application'


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join( BASE_DIR, 'db.sqlite3' ),
    }
}


# Internationalization
LANGUAGE_CODE = 'ja'
TIME_ZONE = 'Asia/Tokyo'
USE_I18N = True
USE_L10N = True
USE_TZ = True




####################################################################################################
# For Gracenote Common Settings
####################################################################################################
# Paths
PACKAGE_ROOT = os.path.abspath( os.path.dirname( __file__ ) )
GRACED_ROOT = os.path.join( PACKAGE_ROOT, "grace.d" )
# LOCK_ROOT = os.path.join(GRACED_ROOT  , "lock")
CONF_ROOT = os.path.join( GRACED_ROOT  , "conf" )
# CERT_ROOT     = os.path.join(GRACED_ROOT  , "cert")
LOG_ROOT = os.path.join( GRACED_ROOT  , "log" )
DATA_ROOT = os.path.join( GRACED_ROOT  , "data" )


# For api setting
# API_CERT            = os.path.join(CERT_ROOT, "cacert.pem")
# API_CONTENT_TYPE    = {"Content-Type":"application/json; charset=utf-8"}
API_CLIENT_ID = ''


# For search batch errrmsg
EMS_BODY = "ERRTYPE={0}  ERRVAL={1}  TRACEBACK={2}"
# EMS_LOCKFILE_EXISTS = "ERRCODE={0}  ERRMSG=Lock file is already exist. LOCKFILE={1}"
# EMS_API_RETRY_OVER = "ERRCODE={0}  ERRMSG=API retry over error. RETRY_COUNT={1}"
# EMS_API_SVRERR = "ERRCODE={0}  ERRMSG=API server error ocurred. API_RESULT={1}"
EMS_SYSTEMERR = "ERRCODE={0}  ERRMSG=System error is occured."


# For search batch errcode
# ECD_LOCKFILE_EXISTS = "E100"
# ECD_API_RANGE = "E200"
# ECD_API_RETRY_OVER = "E700"
# ECD_API_SVRERR = "E701"
ECD_SYSTEMERR = "E900"


# For api return status
# HTTP_OK = 200
# HTTP_BAD_REQUEST            =400
# HTTP_UNAUTHORIZED           =401
# HTTP_NOTFOUND               =404
# HTTP_INTERNAL_SERVER_ERROR  =500
# HTTP_SERVICE_UNAVAILABLE = 503

# For timeformat
# FMT_YYYYMMDDHH24MISS = "%Y%m%d%H%M%S"
# FMT_YYYYMMDDHH24 = "{0:%Y%m%d%H}"
# FMT_YYYYMMDDHH24MISS_2 = "{0:%Y%m%d%H%M%S}"




####################################################################################################
# For hdata_import
####################################################################################################
MZ_LST_FILE = os.path.join( DATA_ROOT, "inputMZ.txt" )


####################################################################################################
# For logging - fomatters, handlers, loggers
####################################################################################################
LOGGING = {
  'version': 1,
  'disable_existing_loggers': True,
  'formatters': {
    'verbose': {
      'format': '%(asctime)s - %(process)d - %(filename)s - %(lineno)d - %(levelname)s - %(message)s'
    },
  },
  'handlers': {
    'null': {
      'level':'DEBUG',
      'class':'logging.NullHandler',
    },
    'console_verbose':{
      'level':'DEBUG',
      'class':'logging.StreamHandler',
      'formatter': 'verbose',
    },
    'file_verbose':{
      'level':'DEBUG',
      'formatter': 'verbose',
      'class':'logging.handlers.RotatingFileHandler',
      'filename': os.path.join( LOG_ROOT, 'gracenote.log' ),
      'maxBytes': 1024 * 1024,
    },
  },
  'loggers': {
    'django': {
      'handlers':['null'],
      'propagate': True,
      'level':'INFO',
    },
    'Gracenote.management.commands.search': {
      'handlers': ['console_verbose', ],
      'level': 'INFO',
    },
    'Gracenote.management.bean.ResultData': {
      'handlers': ['console_verbose', ],
      'level': 'INFO',
    },
  }
}
