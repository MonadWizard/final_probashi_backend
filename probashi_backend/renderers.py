from email import charset
from rest_framework import renderers
import json

class UserRenderer(renderers.JSONRenderer):

    charset='utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = ''
        
        # print('data:::::::::',data)
        # print('renderer:::::::::',renderer_context)
        # print('accepted:::::::::',accepted_media_type)
        # print('status:::::::::',renderer_context['response'].status_code )
        
        
        if 'ErrorDetail' in str(data):
            response = json.dumps({'success': False, 'message': data})
        elif renderer_context['response'].status_code == 400:
            response = json.dumps({'success': False, 'message': data})
        elif renderer_context['response'].status_code == 401:
            response = json.dumps({'success': False, 'message': data})
        elif renderer_context['response'].status_code == 500:
            response = json.dumps({'success': False, 'message': data})

        else:
            response = json.dumps({'success': True, 'data': data})
        return response

        # import pdb
        # pdb.set_trace()

        # return super.render(data, accepted_media_type=accepted_media_type, renderer_context=renderer_context)













