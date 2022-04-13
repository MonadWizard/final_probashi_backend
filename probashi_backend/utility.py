def sql_array_to_object(field_names, values):
    data = {}
    
    for (name, v) in zip(field_names, values):
        data[name] = v
        
    return data