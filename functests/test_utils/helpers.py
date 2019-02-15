# there are some problems with underscored/private fields validation
def replace_id(data: dict):
    object_id_str = data['_id']
    data['id'] = object_id_str
    del data['_id']
    return data
