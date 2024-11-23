from datetime import datetime


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


def str_to_datetime(str_datetime):
    try:
        return datetime.strptime(str_datetime, '%Y-%m-%dT%H:%M:%S.%f')
    except:
        return datetime.strptime(str_datetime, '%Y-%m-%dT%H:%M:%S')
