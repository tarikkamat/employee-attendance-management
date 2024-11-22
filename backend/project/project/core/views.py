from django.http import Http404
from users.models import User
from rest_framework import permissions, serializers
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.args = None
        self.kwargs = None
        self.request = None
        self.headers = {}
        self.response = None

    @staticmethod
    def get_object_or_404(klass, *args, **kwargs):
        return get_queryset_or_404(klass, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.request = self.initialize_request(request, *args, **kwargs)
        self.headers = self.default_response_headers
        try:
            self.initial(self.request, *args, **kwargs)
            if request.method.lower() in self.http_method_names:
                handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed
            response = handler(self.request, *args, **kwargs)
        except Exception as exc:
            response = self.handle_exception(exc)
        self.response = self.finalize_response(self.request, response, *args, **kwargs)
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
        queryset = self.model.objects.url_filter(self.request).filter(is_deleted=False).order_by("id")

        if self.model == User:
            if not self.request.user.is_superuser:
                return queryset.filter(id=self.request.user.id)
            return queryset

        if not self.request.user.is_superuser and hasattr(self.model, "created_by"):
            return queryset.filter(created_by=self.request.user)

        return queryset

    def get(self, request):
        try:
            paginator = self.pagination_class()
            queryset = self.get_queryset()
            paginated_queryset = paginator.paginate_queryset(queryset, request, view=self)
            serializer = self.serializer_class(paginated_queryset, many=True)
            return paginator.get_paginated_response(serializer.data)
        except AttributeError as e:
            return APIResponse.custom_error(f"Pagination error: {str(e)}")

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        try:
            request.data._mutable = True
        except AttributeError:
            pass
        request.data.update({"created_by": request.user.id})

        if serializer.is_valid():
            serializer.save()
            return APIResponse.created(serializer.data)
        return APIResponse.bad_request(serializer.errors)


class BaseDetailView(CustomAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication, TokenAuthentication, SessionAuthentication]
    serializer_class = serializers.ModelSerializer
    model = BaseModel

    def get_object(self, pk):
        obj = self.get_object_or_404(self.model, pk=pk)
        if self.model == User and not self.request.user.is_superuser and obj.pk != self.request.user.pk:
            return APIResponse.unauthorized("You do not have permission to access this user.")

        if hasattr(obj, "created_by") and not self.request.user.is_superuser and obj.created_by != self.request.user:
            return APIResponse.unauthorized("You do not have permission to access this object.")

        return obj

    def get(self, request, pk):
        obj = self.get_object(pk)
        if isinstance(obj, Response):
            return obj
        serializer = self.serializer_class(obj)
        return APIResponse.success(serializer.data)

    def patch(self, request, pk):
        obj = self.get_object(pk)
        if isinstance(obj, Response):
            return obj
        serializer = self.serializer_class(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return APIResponse.success(serializer.data)
        return APIResponse.bad_request(serializer.errors)

    def delete(self, request, pk):
        obj = self.get_object(pk)
        if isinstance(obj, Response):
            return obj
        obj.delete()
        return APIResponse.deleted()
