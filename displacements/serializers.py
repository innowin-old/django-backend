import psycopg2
from psycopg2.extras import DictCursor

from rest_framework.serializers import ModelSerializer, ListField

from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Q
from users.models import Profile, Identity
from products.models import Category, CategoryField, Product


class GetUserDataSerializer(ModelSerializer):
    errors_log = ListField(required=False)

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        conn_string = "host='localhost' dbname='danesh_boom_master' user='postgres' password='1A2b3F4po'"
        # print the connection string we will use to connect
        print("Connecting to database\n	->%s" % conn_string)

        # get a connection, if a connect cannot be made an exception will be raised here
        conn = psycopg2.connect(conn_string, cursor_factory=DictCursor)

        # conn.cursor will return a cursor object, you can use this cursor to perform queries
        cursor = conn.cursor()

        # execute our Query
        cursor.execute("SELECT * FROM auth_user")

        # retrieve the records from the database
        records = cursor.fetchall()

        last_fields = settings.USERS_BEFORE_FIELDS
        errors_log = []

        for record in records:
            kwargs = {}
            for key in last_fields:
                kwargs[key] = record[key]
            try:
                user = User.objects.get(username=kwargs['username'])
            except User.DoesNotExist:
                user = False
            if user:
                errors_log.append('user with username=' + user.username + ' exist !')
            else:
                user = User.objects.create(
                    username=kwargs['username'],
                    first_name=kwargs['first_name'],
                    last_name=kwargs['last_name'],
                    email=kwargs['email'],
                    date_joined=kwargs['date_joined'],
                    is_staff=kwargs['is_staff'],
                    is_active=kwargs['is_active'],
                    password=kwargs['password']
                )
                user.save()
                # update user profile
                profile = Profile.objects.get(profile_user=user)
                cursor.execute("SELECT * FROM users_profile WHERE profile_user_id=%s", (user.id,))
                profile_records = cursor.fetchall()
                before_profile = settings.PROFILES_BEFORE_FIELDS
                for profile_record in profile_records:
                    for key in before_profile:
                        setattr(profile, key, profile_record[key])
                profile.save()
                # update user identity
                identity = Identity.objects.get(identity_user=user)
                cursor.execute("SELECT * FROM users_identity WHERE identity_user_id=%s", (user.id,))
                identity_records = cursor.fetchall()
                before_identity = settings.IDENTITY_BEFORE_FIELDS
                for identity_record in identity_records:
                    for key in before_identity:
                        setattr(profile, key, identity_record[key])
                identity.save()
        user.errors_log = errors_log
        cursor.close()
        conn.close()

        return user


class GetProductDataSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def create(self, validated_data):
        conn_string = "host='localhost' dbname='danesh_boom_master' user='postgres' password='1A2b3F4po'"
        # print the connection string we will use to connect
        print("Connecting to database\n	->%s" % conn_string)

        # get a connection, if a connect cannot be made an exception will be raised here
        conn = psycopg2.connect(conn_string, cursor_factory=DictCursor)

        # conn.cursor will return a cursor object, you can use this cursor to perform queries
        cursor = conn.cursor()

        # execute our Query
        cursor.execute("SELECT * FROM products_category")

        # retrieve the records from the database
        category_records = cursor.fetchall()

        last_fields = settings.CATEGORIES_BEFORE_FIELDS
        errors_log = []

        for category_record in category_records:
            category_kwargs = {}
            for key in last_fields:
                print(category_record[key])
                category_kwargs[key] = category_record[key]
            try:
                category = Category.objects.get(name=category_kwargs['name'])
            except Category.DoesNotExist:
                category = False
            if category:
                errors_log.append('category with username=' + category.name + ' exist !')
            else:
                if category_kwargs['category_parent_id']:
                    cursor.execute("SELECT * FROM products_category WHERE id=%s",
                                   (category_kwargs['category_parent_id'],))
                    category_parent_record = cursor.fetchall()[0]
                    category_parent = Category.objects.get(name=category_parent_record['id'])
                    category_kwargs['category_parent_id'] = category_parent.id
                category = Category.objects.create(
                    category_parent=category_kwargs['category_parent_id'],
                    name=category_kwargs['name'],
                    title=category_kwargs['title'],
                    creatable=category_kwargs['creatable']
                )
                category.save()
                cursor.execute("SELECT * FROM products_category_field WHERE field_category_id=%s",
                               (category_kwargs['id'],))
                category_field_records = cursor.fetchall()
                last_categoryfields_fields = settings.CATEGORY_FIELDS_BEFORE_FIELDS
                for category_field_record in category_field_records:
                    category_field_kwargs = {}
                    for key in last_categoryfields_fields:
                        print(category_field_record[key])
                        category_field_kwargs[key] = category_field_record[key]
                    try:
                        category_field = CategoryField.objects.get(Q(name=category_field_kwargs['name']) |
                                                                   Q(title=category_field_kwargs['title']))
                    except CategoryField.DoesNotExist:
                        category_field = False
                    if category_field:
                        errors_log.append(
                            'category_field with name=' + category_field.name + ' or title=' + category_field.title + ' exist !')
                    else:
                        category_field = CategoryField.objects.create(
                            field_category_id=category.id,
                            name=category_field_kwargs['name'],
                            title=category_field_kwargs['title'],
                            type=category_field_kwargs['type'],
                            order=category_field_kwargs['order'],
                            option=category_field_kwargs['option']
                        )
                        category_field.save()
                cursor.execute("SELECT * FROM products_product WHERE product_category_id=%s", (category_kwargs['id'],))
                product_records = cursor.fetchall()
                last_product_fields = settings.PRODUCT_BEFORE_FIELDS
                for product_record in product_records:
                    product_kwargs = {}
                    for key in last_product_fields:
                        print(key)
                        product_kwargs[key] = product_record[key]
                    cursor.execute("SELECT * FROM users_identity WHERE id=%s", product_kwargs['product_owner_id'])
                    identity_record = cursor.fetchall()[0]
                    try:
                        identity = Identity.objects.get(name=identity_record['name'])
                    except Identity.DoesNotExist:
                        identity = False
                        errors_log.append('identity with name=' + identity_record['name'] + ' in product addition exist !')
                    if identity:
                        product = Product.objects.create(
                            identity=identity,
                            product_category=category,
                            name=product_kwargs['name'],
                            country=product_kwargs['country'],
                            province=product_kwargs['province'],
                            city=product_kwargs['city'],
                            description=product_kwargs['description'],
                            attrs=product_kwargs['attrs'],
                            custom_attrs=product_kwargs['custom_attrs']
                        )
                        product.save()
        cursor.close()
        conn.close()
        # product = Product.objects.create(**validated_data)

        # product.errors_log = errors_log

        # return product
