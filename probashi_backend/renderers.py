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
            # print('data 400:::::::::::',data)
            response = json.dumps({'success': False, 'message': data}, ensure_ascii=False)
        elif renderer_context['response'].status_code == 401:
            # print(data, type(data))
            response = json.dumps({'success': False, 'message': data})
        elif renderer_context['response'].status_code == 500:
            response = json.dumps({'success': False, 'message': data})

        else:
            
            # if type(data) == dict:
            print('response:::::::::',type(data))
            response = {'success': True}
            response.update(data)

            # response = json.dumps({'success': True, 'data': data})
        
        return json.dumps(response)

        # import pdb
        # pdb.set_trace()

        # return super.render(data, accepted_media_type=accepted_media_type, renderer_context=renderer_context)













