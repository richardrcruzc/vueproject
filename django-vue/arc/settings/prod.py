''# from typing import Union
from .base import *


DEBUG=True

DATABASES['default']['NAME'] = 'moe_arc'
DATABASES['default']['USER'] = 'root'
DATABASES['default']['PASSWORD'] = ''

# STATIC_ROOT: Union[bytes, str] = os.path.join(BASE_DIR, 'static')
ALLOWED_HOSTS += ['*']

UPLOAD_FOLDER = os.path.join(BASE_DIR, "files")
UPLOAD_URL = '/files/'

WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'js/',
        'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.prod.json'),
    }
}
