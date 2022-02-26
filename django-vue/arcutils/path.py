from django.utils.deconstruct import deconstructible
from django.conf import settings
from uuid import uuid4
import os, errno


@deconstructible
class UploadToPathAndRename(object):
    def __init__(self, path):
        self.sub_path = path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        local_path = os.path.join(settings.MEDIA_ROOT, self.sub_path)

        try:
            os.makedirs(local_path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        filename = '{}.{}'.format(uuid4().hex, ext)
        return os.path.join(self.sub_path, filename)
