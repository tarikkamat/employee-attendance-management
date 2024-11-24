from django.http import Http404
from rest_framework import permissions, serializers
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from project.core.responses import APIResponse
from project.db.models import BaseModel


def get_queryset_or_404(klass, *args, **kwargs):
    queryset = getattr(klass, "_default_manager", klass)
    if not hasattr(queryset, "get"):
        raise ValueError(f"Invalid argument: {klass}. Must be a Model, Manager, or QuerySet.")
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        raise Http404(f"No {queryset.model._meta.object_name} matches the given query.")


class CustomAPIView(APIView):
    def get_object_or_404(self, klass, *args, **kwargs):
        queryset = _get_queryset(klass)
        if not hasattr(queryset, "get"):
            klass__name = (
                klass.__name__ if isinstance(klass, type) else klass.__class__.__name__
            )
            raise ValueError("First argument to get_object_or_404() must be a Model, Manager, " "or QuerySet, not '%s'." % klass__name)
        try:
            return queryset.get(*args, **kwargs)
        except queryset.model.DoesNotExist:
            raise Http404("No %s matches the given query." % queryset.model._meta.object_name)

    def dispatch(self, request, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        request = self.initialize_request(request, *args, **kwargs)
        self.request = request
        self.headers = self.default_response_headers  # deprecate?
        try:
            self.initial(request, *args, **kwargs)
            # Get the appropriate handler method
            if request.method.lower() in self.http_method_names:
                handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed
            response = handler(request, *args, **kwargs)
        except Exception as exc:
            response = self.handle_exception(exc)
        self.response = self.finalize_response(request, response, *args, **kwargs)
        try:
            if hasattr(request.user, 'email'):
                add_activity_log(request=request, response=self.response)
        except:
            pass
        return self.response

    class Meta:
        abstract = True


class CustomListView(ListAPIView, CustomAPIView):
    class Meta:
        abstract = True


class BaseListView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication, TokenAuthentication, SessionAuthentication]
    pagination_class = PageNumberPagination

    serializer_class = serializers.ModelSerializer
    model = BaseModel

    def get_queryset(self):
        queryset = self.model.objects.url_filter(self.request).filter(is_deleted=False)

        if self.request.user.is_superuser:
            return queryset.order_by('id')

        if hasattr(self.model, 'fk_user_id'):
            return queryset.filter(fk_user_id=self.request.user.id).order_by('id')

        return queryset.order_by('id')

    def get(self, request):
        pagination_class = self.pagination_class()
        pagination_class.page_query_param = "page"
        pagination_class.page_size_query_param = 'page_size'
        context = pagination_class.paginate_queryset(self.get_queryset(), request)
        serializer = self.serializer_class(context, many=True)
        return pagination_class.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return APIResponse.created(serializer)
        return APIResponse.bad_request(serializer)

    class Meta:
        abstract = True


class BaseDetailView(CustomAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication, TokenAuthentication, SessionAuthentication]

    serializer_class = serializers.ModelSerializer
    model = BaseModel

    def get_queryset(self, pk):
        return self.model.objects.get(pk=pk)

    def get(self, request, pk):
        serializer = self.serializer_class(self.get_queryset(pk=pk))
        return APIResponse.success(serializer)

    def patch(self, request, pk):
        instance = self.model.objects.get(id=pk)
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return APIResponse.success(serializer)
        return APIResponse.bad_request(serializer)

    def delete(self, request, pk):
        instance = self.model.objects.get(id=pk)
        instance.delete()
        return APIResponse.deleted()

    class Meta:
        abstract = True
