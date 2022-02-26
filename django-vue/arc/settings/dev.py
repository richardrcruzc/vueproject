from .base import *

DEBUG = True

DATABASES['default']['USER'] = 'root'
DATABASES['default']['PASSWORD'] = 'root'

INTERNAL_IPS = ['127.0.0.1']

ALLOWED_HOSTS += INTERNAL_IPS
ALLOWED_HOSTS += ['localhost', '192.168.1.7', '221.220.200.77']

INSTALLED_APPS += [
    'webpack_loader',
    'debug_toolbar',
]

MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']

DATABASES['default']['PASSWORD'] = ''

UPLOAD_FOLDER = os.path.join(BASE_DIR, "files")
UPLOAD_URL = '/files/'

WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'dist/',
        'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.json'),
    }
}
