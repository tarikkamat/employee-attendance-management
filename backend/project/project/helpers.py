from datetime import datetime

"""
This function returns the slug of a model in the API

:param model: model object
:return: slug of the model in the API
"""


def get_api_slug(model=object):
    verbose_name = model._meta.verbose_name
    model_slug = verbose_name.replace(' ', '_')
    if model_slug[-1] == 's' or model_slug[-1] == 'h':
        model_slug = model_slug + 'es'
    elif model_slug[-1] == 'y':
        model_slug = model_slug[:-1] + 'ies'
    else:
        model_slug = model_slug + 's'
    return model_slug


"""
This function converts a string datetime to a datetime object

:param str_datetime: string datetime
:return: datetime object
"""


def str_to_datetime(str_datetime):
    try:
        return datetime.strptime(str_datetime, '%Y-%m-%dT%H:%M:%S.%f')
    except:
        return datetime.strptime(str_datetime, '%Y-%m-%dT%H:%M:%S')
