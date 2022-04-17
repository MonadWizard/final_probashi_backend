def sql_array_to_object(field_names, values):
    data = {}
    
    for (name, v) in zip(field_names, values):
        data[name] = v
        
        if data.get('is_text_message') == True:
            data['message-type'] = 'text'
            data.pop('is_text_message')


        if data.get('is_text_message') == False:
            data.pop('is_text_message')
        if data.get('is_file_message') == False:
            data.pop('is_file_message')
        if data.get('is_audio_message') == False:
            data.pop('is_audio_message')
        if data.get('is_image_message') == False:
            data.pop('is_image_message')


    # print('data:::::', data)

    return data