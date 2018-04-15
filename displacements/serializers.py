from sqlite3 import Cache

import psycopg2
from psycopg2.extras import DictCursor

from rest_framework.serializers import ModelSerializer, ListField

from django.contrib.auth.models import User
from django.conf import settings
from users.models import Profile, Identity
from products.models import Product, CategoryField, Category, Price, Comment


class GetUserDataSerializer(ModelSerializer):
    errors_log = ListField(required=False)

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        conn_string = "host='localhost' dbname='" + settings.LAST_DATABASE_NAME + "' user='" + settings.LAST_DATABASE_USERNAME + "' password='" + settings.LAST_DATABASE_PASSWORD + "'"
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
    errors_log = ListField(required=False)

    class Meta:
        model = Category
        fields = '__all__'

    def create(self, validated_data):
        conn_string = "host='localhost' dbname='" + settings.LAST_DATABASE_NAME + "' user='" + settings.LAST_DATABASE_USERNAME + "' password='" + settings.LAST_DATABASE_PASSWORD + "'"
        # print the connection string we will use to connect
        print("Connecting to database\n	->%s" % conn_string)

        # get a connection, if a connect cannot be made an exception will be raised here
        conn = psycopg2.connect(conn_string, cursor_factory=DictCursor)

        # conn.cursor will return a cursor object, you can use this cursor to perform queries
        cursor = conn.cursor()

        # execute our Query
        cursor.execute("SELECT * FROM products_category")

        # retrieve the records from the database
        records = cursor.fetchall()

        last_fields = settings.CATEGORY_BEFORE_FIELDS
        errors_log = []

        for record in records:
            kwargs = {}
            for key in last_fields:
                kwargs[key] = record[key]
            try:
                category = Category.objects.get(name=kwargs['name'])
            except Category.DoesNotExist:
                category = False
            if category:
                print('error logged !!!')
                errors_log.append('category with name=' + category.name + ' already exist !')
            else:
                category = Category.objects.create(
                    name=kwargs['name'],
                    title=kwargs['title'],
                    creatable=kwargs['creatable']
                )
                category.save()
                # add category fields
                print('add category fields')
                cursor.execute("SELECT * FROM products_categoryfield WHERE field_category_id=%s", (kwargs['base_ptr_id'],))
                category_fields_records = cursor.fetchall()
                category_fields_before = settings.PRODUCTS_BEFORE_FIELDS
                for category_fields_record in category_fields_records:
                    category_fields_kwargs = {}
                    for key in category_fields_before:
                        category_fields_kwargs[key] = category_fields_record[key]
                    try:
                        category_field = CategoryField.objects.get(name=category_fields_kwargs['name'])
                    except CategoryField.DoesNotExist:
                        category_field = False
                    if category_field:
                        print('error logged !!!')
                        errors_log.append('category field with name=' + category_field.name + ' already exist !')
                    else:
                        category_field = CategoryField.objects.create(
                            field_category=category,
                            name=category_fields_kwargs['name'],
                            title=category_fields_kwargs['title'],
                            type=category_fields_kwargs['type'],
                            order=category_fields_kwargs['order'],
                            option=category_fields_kwargs['option']
                        )
                        category_field.save()
                # add products
                print('add products')
                cursor.execute("SELECT * FROM products_product WHERE product_category_id=%s", (kwargs['base_ptr_id'],))
                product_records = cursor.fetchall()
                products_before = settings.PRODUCTS_BEFORE_FIELDS
                for product_record in product_records:
                    product_kwargs = {}
                    for key in products_before:
                        product_kwargs[key] = product_record[key]
                    cursor.execute("SELECT * FROM users_identity WHERE base_ptr_id=%s", (product_kwargs['product_owner_id'],))
                    identity_records = cursor.fetchall()
                    for identity_record in identity_records:
                        identity_name = identity_record['name']
                    try:
                        identity = Identity.objects.get(name=identity_name)
                    except Identity.DoesNotExist:
                        identity = {'id': 1}
                        print('error logged !!!')
                        errors_log.append('category field with name=' + identity_name + ' already exist !')
                    product = Product.objects.create(
                        product_owner_id=identity.id,
                        product_category_id=category.id,
                        name=product_kwargs['name'],
                        country=product_kwargs['country'],
                        province=product_kwargs['province'],
                        city=product_kwargs['city'],
                        description=product_kwargs['description'],
                        attrs=product_kwargs['attrs'],
                        custom_attrs=product_kwargs['custom_attrs']
                    )
                    product.save()
                    # add prices
                    print('add prices')
                    cursor.execute("SELECT * FROM products_price WHERE price_product_id=%s", (product_kwargs['base_ptr_id'],))
                    price_records = cursor.fetchall()
                    prices_before = settings.PRICES_BEFORE_FIELDS
                    for price_record in price_records:
                        price_kwargs = {}
                        for key in prices_before:
                            price_kwargs[key] = price_record[key]
                        price = Price.objects.create(
                            price_product_id=product.id,
                            value=price_kwargs['value']
                        )
                        price.save()
                    # add pictures
                    '''cursor.execute("SELECT * FROM products_picture WHERE picture_product_id=%", (product_kwargs['id'],))
                    picture_records = cursor.fetchall()
                    picture_before = settings.PRICES_BEFORE_FIELDS
                    for picture_record in picture_records:
                        picture_kwargs = {}
                        for key in picture_before:
                            picture_kwargs[key] = picture_record[key]
                        picture = Picture.objects.create(
                            picture_product_id=product.id,
                            value=picture_record['value']
                        )
                        price.save()'''
                    # add comments
                    print('add comments')
                    cursor.execute("SELECT * FROM products_comment WHERE comment_product_id=%s", (product_kwargs['base_ptr_id'],))
                    comment_records = cursor.fetchall()
                    comments_before = settings.PRICES_BEFORE_FIELDS
                    for comment_record in comment_records:
                        comment_kwargs = {}
                        for key in comments_before:
                            comment_kwargs[key] = comment_record[key]
                        cursor.execute("SELECT * FROM users_user WHERE id=%s", (comment_kwargs['comment_user_id'],))
                        user_records = cursor.fetchall()
                        for user_record in user_records:
                            user_username = user_record['username']
                        user = User.objects.filter(username=user_username)
                        user = user[0]
                        comment = Comment.objects.create(
                            comment_product_id=product.id,
                            comment_user_id=user.id,
                            text=comment_kwargs['text']
                        )
                        comment.save()
        # fill parents
        cursor.execute("SELECT * FROM products_category")
        # retrieve the records from the database
        category_parent_records = cursor.fetchall()
        for category_parent_record in category_parent_records:
            category_parent_kwargs = {}
            for key in last_fields:
                category_parent_kwargs[key] = category_parent_record[key]
        if category_parent_kwargs['category_parent_id'] is not None or category_parent_kwargs['category_parent_id'] != '':
            cursor.execute("SELECT * FROM products_category WHERE base_ptr_id=%s",
                           (category_parent_kwargs['base_ptr_id'],))
            parent_records = cursor.fetchall()
            for parent_record in parent_records:
                parent_name = parent_record['name']
            try:
                parent_object = Category.objects.get(name=parent_name)
            except Category.DoesNotExist:
                parent_object = None
                errors_log.append('category parent with ame=' + parent_name + ' already exist !')
            if parent_object is not None:
                try:
                    category_parent = Category.objects.get(name=category_parent_kwargs['name'])
                except Category.DoesNotExist:
                    category_parent = False
                    errors_log.append(
                        'category parent with name=' + parent_name + ' on target not exist !')
                if category_parent:
                    category_parent.category_parent_id = parent_object.id
                    category_parent.save()
        category.errors_log = errors_log
        cursor.close()
        conn.close()
        return category