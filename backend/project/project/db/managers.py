from django.db import models
from django.db.models import Q

from project.helpers import str_to_datetime


class BaseManager(models.Manager):

    def filter(self, *args, **kwargs):
        return super().filter(*args, **kwargs)

    def url_filter(self, request):
        query = Q()
        for param, value in request.query_params.items():
            if param == 'page' or param == 'depth' or param == 'page_size':
                continue
            if '__' in param or self.model._meta.get_field(str(param).split('__')[0]).get_internal_type() in ['ForeignKey']:
                if '__gte' in param or '__gt' in param or '__lte' in param or '__lt' in param:
                    try:
                        query = query & Q(**{str(param): str_to_datetime(value)})
                    except:
                        query = query & Q(**{str(param): value})
                else:
                    if '__' in param:
                        query = query & Q(**{str(param) + "__contains": value})
                    else:
                        query = query & Q(**{str(param) + "__id__contains": value})
            else:
                query = query & Q(**{str(param) + "__contains": value})
        return self.filter(query)

    class Meta:
        abstract = True
