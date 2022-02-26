from django.http import JsonResponse

from arcutils.dict_helper import define_word
from .base import ProtectedView


class ToolsApi(ProtectedView):
    def get(self, request, **kwargs):
        if 'tool_name' in kwargs:
            if kwargs['tool_name'] == 'dict' and 'tool_param' in kwargs:
                retval = define_word(kwargs['tool_param'])
                if retval['status'] == 0:
                    return JsonResponse({'status': 0, 'def': retval['definition']})

        return JsonResponse({'status': 1, 'error_code': 1})
