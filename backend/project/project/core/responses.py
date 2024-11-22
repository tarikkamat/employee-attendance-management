from rest_framework import status
from rest_framework.response import Response


class APIResponse:
    """
    A utility class for consistent API responses.
    Provides static methods for generating common HTTP responses.
    """

    @staticmethod
    def success(data):
        """Returns a 200 OK response with serialized data."""
        return Response(data, status=status.HTTP_200_OK)

    @staticmethod
    def created(data):
        """Returns a 201 Created response with serialized data."""
        return Response(data, status=status.HTTP_201_CREATED)

    @staticmethod
    def deleted():
        """Returns a 204 No Content response indicating a successful deletion."""
        return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def bad_request(errors):
        """Returns a 400 Bad Request response with validation errors."""
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def custom_error(message, status_code=status.HTTP_400_BAD_REQUEST):
        """Returns a custom error response with a given status code."""
        return Response({"message": message}, status=status_code)

    @staticmethod
    def unauthorized(message="Unauthorized"):
        """Returns a 401 Unauthorized response."""
        return Response({"message": message}, status=status.HTTP_401_UNAUTHORIZED)

    @staticmethod
    def forbidden(message="Forbidden"):
        """Returns a 403 Forbidden response."""
        return Response({"message": message}, status=status.HTTP_403_FORBIDDEN)
