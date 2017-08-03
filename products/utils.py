from utils.Exceptions import ResponseError
import json
from products.models import CategoryField


def add_attrs(primary_attrs, category):
    attrs = {}
    limit_character = 100
    if primary_attrs:
        for i in range(0, primary_attrs.__len__()):
            name = primary_attrs[i].get('name')
            value = primary_attrs[i].get('value', '')
            if value and len(value) > limit_character:
                raise ResponseError(
                    "Number of value characters is exceeded",
                    code='invalid_attrs'
                )
            category_field = CategoryField.objects.filter(name__exact=name).first()
            if not category_field or category != category_field.category:
                raise ResponseError(
                    "Invalid Category field",
                    code='invalid_category_field')
            else:
                title = category_field.title
                type_ = category_field.type
                order = category_field.order
                option = category_field.option
                attrs[name] = {
                    "title": title,
                    "type": type_,
                    "order": order,
                    "option": option,
                    "value": value
                }
    json_attrs = json.dumps(attrs)
    return json_attrs


def add_custom_attrs(primary_custom_attrs):
    custom_attrs = {}
    limit_array = 50
    limit_character = 100
    if primary_custom_attrs:
        if primary_custom_attrs.__len__() < limit_array:
            for i in range(0, primary_custom_attrs.__len__()):
                key = primary_custom_attrs[i].get('name')
                value = primary_custom_attrs[i].get('value')
                if key and value:
                    if len(key) > limit_character or len(value) > limit_character:
                        raise ResponseError(
                            "Number of characters exceeds the limit",
                            code='invalid_custom_attrs'
                        )
                    custom_attrs[key] = value
                else:
                    raise ResponseError(
                        "Key or value is empty",
                        code='invalid_custom_attrs'
                    )
        else:
            raise ResponseError(
                "Number of array elements is exceeded",
                code='invalid_custom_attrs'
            )
    json_custom_attrs = json.dumps(custom_attrs)
    return json_custom_attrs


def check_superuser(context):
    user = context.user
    if not user.is_superuser:
        raise ResponseError(
            "This user is not super user",
            code=' not_access_permission')
