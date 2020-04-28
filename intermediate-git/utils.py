def get_forms_dict(request_forms):
    return {key: getattr(request_forms, key) for key in request_forms}
