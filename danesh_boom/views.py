import traceback

from django.conf import settings
from graphene_django.views import GraphQLView
from graphql.error import GraphQLSyntaxError
from graphql.error.located_error import GraphQLLocatedError
from graphql.error import format_error as format_graphql_error
from utils.Exceptions import ResponseError

from rest_framework_jwt.views import ObtainJSONWebToken

from .serializers import JWTSerializer


def format_response_error(error: ResponseError):
    return {
        'message': error.message,
        'code': error.code,
        'params': error.params,
    }


def format_internal_error(error: Exception):
    message = 'Internal server error'
    code = 'internal-server-error'
    if settings.DEBUG:
        params = {
            'exception': type(error).__name__,
            'message': str(error),
            'trace': traceback.format_list(traceback.extract_tb(error.__traceback__)),
        }
        return {
            'code': code,
            'message': message,
            'params': params,
        }
    return {
        'code': code,
        'message': message,
    }


def format_located_error(error):
    if isinstance(error.original_error, GraphQLLocatedError):
        return format_located_error(error.original_error)
    if isinstance(error.original_error, ResponseError):
        return format_response_error(error.original_error)
    return format_internal_error(error.original_error)


class SafeGraphQLView(GraphQLView):
    @staticmethod
    def format_error(error):
        try:
            if isinstance(error, GraphQLLocatedError):
                return format_located_error(error)
            if isinstance(error, GraphQLSyntaxError):
                return format_graphql_error(error)
        except Exception as e:
            return format_internal_error(e)


class ObtainJWTView(ObtainJSONWebToken):
    serializer_class = JWTSerializer