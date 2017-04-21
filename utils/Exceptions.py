import re
from graphene.utils.str_converters import to_camel_case

from utils.str_converters import to_kebab_case, dict_key_to_camel_case


def encode_code(code):
    if code is None:
        return None
    return to_kebab_case(code)


def encode_params(params):
    if params is None:
        return None
    return dict_key_to_camel_case(params)


def encode_field(field):
    return re.sub(r'__$', '_', to_camel_case(field))


class ResponseError(Exception):
    def __init__(self, message, code=None, params=None):
        super().__init__(message)
        self.message = str(message)
        self.code = encode_code(code)
        self.params = encode_params(params)


class FormError(ResponseError):
    @staticmethod
    def format_field_error(err):
        return {
            'code': encode_code(err.code),
            'params': encode_params(err.params),
            'message': str(err.message),
        }

    @staticmethod
    def format_field_errors(field, errs):
        return [
            encode_field(field),
            [FormError.format_field_error(err) for err in errs],
        ]

    def __init__(self, form_errors):
        params = {
            'form_errors': [
                FormError.format_field_errors(field, errs) for field, errs in form_errors.as_data().items()
            ]
        }
        super().__init__(message='Form Error', code='form_error', params=params)
