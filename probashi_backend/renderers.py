from rest_framework import renderers
import json


class UserRenderer(renderers.JSONRenderer):

    charset='utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = ''
        
        # print('data:::::::::', data)
        # print('renderer:::::::::',renderer_context)
        # print('accepted:::::::::',accepted_media_type)
        # print('status:::::::::',renderer_context['response'].status_code )
        
        
        if 'ErrorDetail' in str(data):
            # err = list(list(data.values())[:1])[0]
            # errr2 = list(data.items())[0][1]
            # err = str(err)
            # err2 = 
            print('data erroe:::::::::::',data)
            response = json.dumps({'success': False, 'message':data})
        elif renderer_context['response'].status_code == 400:
            # print('data 400:::::::::::',data)
            # err = list(list(data.values())[:1])[0]
            response = json.dumps({'success': False, 'message': data})
        elif renderer_context['response'].status_code == 401:
            # err = list(list(data.values())[:1])[0]
            # print('data 401:::::::::::',data)

            # print(data, type(data))
            response = json.dumps({'success': False, 'message': data})

        elif renderer_context['response'].status_code == 404:
            response = json.dumps({'success': False, 'message': data})

        elif renderer_context['response'].status_code == 500:
            # err = list(list(data.values())[:1])[0]
            response = json.dumps({'success': False, 'message': data})

        else:
            response = {'success': True}
            response.update(data)

            # response = json.dumps({'success': True, 'data': data})
        
            return json.dumps(response)
        return response

        # import pdb
        # pdb.set_trace()

        # return super.render(data, accepted_media_type=accepted_media_type, renderer_context=renderer_context)













