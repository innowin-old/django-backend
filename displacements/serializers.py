import psycopg2
from psycopg2.extras import DictCursor

from rest_framework.serializers import ModelSerializer, ListField

from django.contrib.auth.models import User
from django.conf import settings

from exchanges.models import Exchange
from users.models import Profile, Identity
from organizations.models import Organization, StaffCount, Staff, Ability, Customer, Confirmation, Follow
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


class GetOrganizationDataSerializer(ModelSerializer):
    errors_log = ListField(required=False)

    class Meta:
        model = Organization
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
        cursor.execute("SELECT * FROM organizations_organization")

        # retrieve the records from the database
        records = cursor.fetchall()

        last_fields = settings.ORGANIZATION_BEFORE_FIELDS
        errors_log = []

        for record in records:
            print('in organization addition')
            kwargs = {}
            for key in last_fields:
                kwargs[key] = record[key]
            try:
                organization = Organization.objects.get(username=kwargs['username'])
            except Organization.DoesNotExist:
                organization = False
            if organization:
                print('error logged !!!')
                errors_log.append('organization with name=' + organization.username + ' already exist !')
            else:
                cursor.execute("SELECT * FROM auth_user WHERE id=%s", (kwargs['owner_id'],))
                owner_records = cursor.fetchall()
                for owner_record in owner_records:
                    owner_username = owner_record['username']
                try:
                    owner_object = User.objects.get(username=owner_username)
                except User.DoesNotExist:
                    owner_object = False
                if not owner_object:
                    print('error logged !!!')
                    errors_log.append('user with username=' + owner_object.username + ' not exist !')
                else:
                    organization = Organization.objects.create(
                        owner_id=owner_object.id,
                        username=kwargs['username'],
                        email=kwargs['email'],
                        nike_name=kwargs['nike_name'],
                        official_name=kwargs['official_name'],
                        national_code=kwargs['national_code'],
                        registration_ads_url=kwargs['registration_ads_url'],
                        registrar_organization=kwargs['registrar_organization'],
                        country=kwargs['country'],
                        province=kwargs['province'],
                        city=kwargs['city'],
                        address=kwargs['address'],
                        phone=kwargs['phone'],
                        web_site=kwargs['web_site'],
                        established_year=kwargs['established_year'],
                        ownership_type=kwargs['ownership_type'],
                        business_type=kwargs['business_type'],
                        biography=kwargs['biography'],
                        description=kwargs['description'],
                        correspondence_language=kwargs['correspondence_language'],
                        social_network=kwargs['social_network'],
                        staff_count=kwargs['staff_count']
                    )
                    cursor.execute("SELECT * FROM organizations_organization_admins WHERE organization_id=%s", (kwargs['base_ptr_id'],))
                    admins_records = cursor.fetchall()
                    for admins_record in admins_records:
                        print('in organization admin addition')
                        admins_id = admins_record['user_id']
                        cursor.execute("SELECT * FROM auth_user WHERE id=%s", (admins_id,))
                        admins_username_records = cursor.fetchall()
                        for admins_username_record in admins_username_records:
                            admins_username = admins_username_record['username']
                            try:
                                admin_object = User.objects.get(username=admins_username)
                            except User.DoesNotExist:
                                admin_object = False
                            if not admin_object:
                                print('error logged !!!')
                                errors_log.append('user with username=' + owner_object.username + ' not exist !')
                            else:
                                organization.admins.add(admin_object)
                    organization.save()
            cursor.execute("SELECT * FROM organizations_staffcount WHERE staff_count_organization_id=%s", (kwargs['base_ptr_id'],))
            staff_count_records = cursor.fetchall()
            staff_count_before = settings.STAFF_COUNT_BEFORE_FIELDS
            for staff_count_record in staff_count_records:
                print('in organization staff count addition')
                staff_count_kwargs = {}
                for staff_count_key in staff_count_before:
                    staff_count_kwargs[staff_count_key] = staff_count_record[staff_count_key]
                cursor.execute("SELECT * FROM organizations_organization WHERE base_ptr_id=%s", (staff_count_kwargs['staff_count_organization_id'],))
                staff_count_organizations_records = cursor.fetchall()
                for staff_count_organizations_record in staff_count_organizations_records:
                    staff_count_organizations_username = staff_count_organizations_record['username']
                try:
                    staff_count_organization_object = Organization.objects.get(username=staff_count_organizations_username)
                except Organization.DoesNotExist:
                    staff_count_organization_object = False
                if not staff_count_organization_object:
                    print('error logged !!!')
                    errors_log.append('user with username=' + staff_count_organizations_username + ' not exist !')
                else:
                    staff_count = StaffCount.objects.create(
                        staff_count_organization_id=staff_count_organization_object.id,
                        count=staff_count_kwargs['count']
                    )
                    staff_count.save()
            cursor.execute("SELECT * FROM organizations_staff WHERE staff_organization_id=%s", (kwargs['base_ptr_id'],))
            staff_records = cursor.fetchall()
            staff_before = settings.STAFF_BEFORE_FIELDS
            for staff_record in staff_records:
                print('in organization staff addition')
                staff_kwargs = {}
                for staff_key in staff_before:
                    staff_kwargs[staff_key] = staff_record[staff_key]
                cursor.execute("SELECT * FROM organizations_organization WHERE base_ptr_id=%s", (staff_kwargs['staff_organization_id'],))
                staff_organizations_records = cursor.fetchall()
                for staff_organizations_record in staff_organizations_records:
                    staff_organizations_username = staff_organizations_record['username']
                try:
                    staff_organization_object = Organization.objects.get(
                        username=staff_organizations_username)
                except Organization.DoesNotExist:
                    staff_organization_object = False
                if not staff_organization_object:
                    print('error logged !!!')
                    errors_log.append('user with username=' + staff_count_organizations_username + ' not exist !')
                else:
                    print('in organization staff auth_user addition')
                    cursor.execute("SELECT * FROM auth_user WHERE id=%s", (staff_kwargs['staff_user_id'],))
                    staff_user_records = cursor.fetchall()
                    for staff_user_record in staff_user_records:
                        staff_user_username = staff_user_record['username']
                    try:
                        staff_user_object = User.objects.get(username=staff_user_username)
                    except User.DoesNotExist:
                        staff_user_object = False
                    if not staff_user_object:
                        print('error logged !!!')
                        errors_log.append('user with username=' + staff_count_organizations_username + ' not exist !')
                    else:
                        staff = Staff.objects.create(
                            staff_organization_id=staff_organization_object.id,
                            staff_user_id=staff_user_object.id,
                            position=staff_kwargs['position'],
                            post_permission=staff_kwargs['post_permission']
                        )
                        staff.save()
            cursor.execute("SELECT * FROM organizations_ability WHERE ability_organization_id=%s", (kwargs['base_ptr_id'],))
            ability_records = cursor.fetchall()
            ability_before = settings.ABILLITY_BEFORE_FIELDS
            for ability_record in ability_records:
                print('in organization ability addition')
                ability_kwargs = {}
                for ability_key in ability_before:
                    ability_kwargs[ability_key] = ability_record[ability_key]
                cursor.execute("SELECT * FROM organizations_organization WHERE base_ptr_id=%s", (ability_kwargs['ability_organization_id'],))
                ability_organizations_records = cursor.fetchall()
                for ability_organizations_record in ability_organizations_records:
                    ability_organizations_username = ability_organizations_record['username']
                try:
                    ability_organization_object = Organization.objects.get(
                        username=ability_organizations_username)
                except Organization.DoesNotExist:
                    ability_organization_object = False
                if not ability_organization_object:
                    print('error logged !!!')
                    errors_log.append('user with username=' + ability_organizations_username + ' not exist !')
                else:
                    ability = Ability.objects.create(
                        ability_organization_id=ability_organization_object.id,
                        title=ability_kwargs['title'],
                        text=ability_kwargs['text']
                    )
                    ability.save()
            cursor.execute("SELECT * FROM organizations_customer WHERE customer_organization_id=%s", (kwargs['base_ptr_id'],))
            customer_records = cursor.fetchall()
            customer_before = settings.CUSTOMER_BEFORE_FIELDS
            for customer_record in customer_records:
                print('in organization customer addition')
                customer_kwargs = {}
                for customer_key in customer_before:
                    customer_kwargs[customer_key] = customer_record[customer_key]
                cursor.execute("SELECT * FROM organizations_organization WHERE base_ptr_id=%s", (customer_kwargs['customer_organization_id'],))
                customer_organizations_records = cursor.fetchall()
                for customer_organizations_record in customer_organizations_records:
                    customer_organizations_username = customer_organizations_record['username']
                try:
                    customer_organization_object = Organization.objects.get(
                        username=customer_organizations_username)
                except Organization.DoesNotExist:
                    customer_organization_object = False
                if not customer_organization_object:
                    print('error logged !!!')
                    errors_log.append('user with username=' + customer_organizations_username + ' not exist !')
                else:
                    cursor.execute("SELECT * FROM users_identity WHERE identity_organization_id=%s", (customer_kwargs['related_customer_id'],))
                    identity_organizations_records = cursor.fetchall()
                    if len(identity_organizations_records) == 0:
                        print('error logged !!!')
                        errors_log.append('user not exist !')
                    else:
                        for identity_organizations_record in identity_organizations_records:
                            #identity_organizations_id = identity_organizations_record['base_ptr_id']
                            identity_organizations_name = identity_organizations_record['name']
                        try:
                            identity_organization_object = Identity.objects.get(name=identity_organizations_name)
                        except Identity.DoesNotExist:
                            identity_organization_object = False
                        if not identity_organization_object:
                            print('error logged !!!')
                            errors_log.append('identity with username=' + identity_organizations_name + ' not exist !')
                        else:
                            customer = Customer.objects.create(
                                customer_organization_id=customer_organization_object.id,
                                related_customer_id=identity_organization_object.id,
                                title=customer_kwargs['title']
                            )
                            customer.save()
        # execute our Query
        cursor.execute("SELECT * FROM organizations_follow")

        # retrieve the records from the database
        follow_records = cursor.fetchall()

        follow_last_fields = settings.FOLLOW_BEFORE_FIELD
        for follow_record in follow_records:
            print('in follow addition')
            follow_kwargs = {}
            for follow_key in follow_last_fields:
                follow_kwargs[follow_key] = follow_record[follow_key]
            cursor.execute("SELECT * FROM users_identity WHERE identity_user_id=%s", (follow_kwargs['follow_identity_id'],))
            identity_follow_records = cursor.fetchall()
            if len(identity_follow_records) == 0:
                print('error logged')
            else:
                for identity_follow_record in identity_follow_records:
                    identity_follow_name = identity_follow_record['name']
                try:
                    identity_follow_object = Identity.objects.get(name=identity_follow_name)
                except Identity.DoesNotExist:
                    identity_follow_object = False
                if not identity_follow_object:
                    print('error logged !!!')
                    errors_log.append('identity with username=' + identity_follow_name + ' not exist !')
                else:
                    cursor.execute("SELECT * FROM users_identity WHERE identity_user_id=%s", (follow_kwargs['follow_identity_id'],))
                    follow_follower_records = cursor.fetchall()
                    for follow_follower_record in follow_follower_records:
                        follow_follower_name = follow_follower_record['name']
                    try:
                        follow_follower_object = Identity.objects.get(
                            name=follow_follower_name)
                    except Identity.DoesNotExist:
                        follow_follower_object = False
                    if not follow_follower_object:
                        print('error logged !!!')
                        errors_log.append(
                            'identity with username=' + follow_follower_name + ' not exist !')
                    else:
                        follow = Follow.objects.create(
                            follow_follower_id=follow_follower_object.id,
                            follow_identity_id=follow_follower_object.id
                        )
                        follow.save()
        # execute our Query
        cursor.execute("SELECT * FROM organizations_confirmation")

        # retrieve the records from the database
        confirmation_records = cursor.fetchall()

        confirmation_last_fields = settings.CONFIRMATION_BEFORE_FIELD
        for confirmation_record in confirmation_records:
            print('in confirmation addition')
            confirmation_kwargs = {}
            for confirmation_key in confirmation_last_fields:
                confirmation_kwargs[confirmation_key] = confirmation_record[confirmation_key]
            cursor.execute("SELECT * FROM user_identity WHERE identity_user_id=%s", (confirmation_kwargs['confirmation_corroborant_id'],))
            identity_confirmation_corroborant_records = cursor.fetchall()
            for identity_confirmation_corroborant_record in identity_confirmation_corroborant_records:
                identity_confirmation_corroborant_name = identity_confirmation_corroborant_record['name']
            try:
                identity_confirmation_corroborant_object = Identity.objects.get(name=identity_confirmation_corroborant_name)
            except Identity.DoesNotExist:
                identity_confirmation_corroborant_object = False
            if not identity_confirmation_corroborant_object:
                print('error logged !!!')
                errors_log.append('identity with username=' + identity_confirmation_corroborant_name + ' not exist !')
            else:
                cursor.execute("SELECT * FROM user_identity WHERE identity_user_id=%s", (confirmation_kwargs['confirmation_confirmed_id'],))
                confirmation_confirmed_records = cursor.fetchall()
                for confirmation_confirmed_record in confirmation_confirmed_records:
                    confirmation_confirmed_name = confirmation_confirmed_record['name']
                try:
                    identity_confirmation_confirmed_object = Identity.objects.get(name=confirmation_confirmed_name)
                except Identity.DoesNotExist:
                    identity_confirmation_confirmed_object = False
                if not identity_confirmation_confirmed_object:
                    print('error logged !!!')
                    errors_log.append('identity with username=' + identity_confirmation_corroborant_name + ' not exist !')
                else:
                    confirmation = Confirmation.objects.create(
                        confirmation_corroborant_id=identity_confirmation_corroborant_object.id,
                        confirmation_confirmed_id=identity_confirmation_confirmed_object.id,
                        title=confirmation_kwargs['title'],
                        description=confirmation_kwargs['description'],
                        link=confirmation_kwargs['link'],
                        confirm_flag=confirmation_kwargs['confirm_flag']
                    )
                    confirmation.save()
        return organization


class GetExchangeDataSerializer(ModelSerializer):
    errors_log = ListField(required=False)

    class Meta:
        model = Exchange
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
        cursor.execute("SELECT * FROM exchanges_exchange")

        # retrieve the records from the database
        exchange_records = cursor.fetchall()

        exchange_before_fields = settings.EXCHANGE_BEFORE_FIELD
        errors_log = []

        for exchange_record in exchange_records:
            exchange_kwargs = {}
            for exchange_key in exchange_before_fields:
                exchange_kwargs[exchange_key] = exchange_record[exchange_key]
            cursor.execute("SELECT * FROM users_identity WHERE base_ptr_id=%s", (exchange_kwargs['owner_id'],))
            exchange_identity_records = cursor.fetchall()
            if len(exchange_identity_records) == 0:
                print('error logged !!!')
                print('identity id = ' + exchange_kwargs['owner_id'] + ' in source data base not found')
            else:
                for exchange_identity_record in exchange_identity_records:
                    exchange_identity_name = exchange_identity_record['name']
                try:
                    exchange_identity_object = Identity.objects.get(name=exchange_identity_name)
                except Identity.DoesNotExist:
                    exchange_identity_object = False
                if not exchange_identity_object:
                    print('error logged !!!')
                    print('identity name=' + exchange_identity_name + 'not found in target data base')
                else:
                    exchange = Exchange.objects.create(
                        name=exchange_record['name'],
                        owner_id=exchange_record['owner_id'],
                        link=exchange_record['link'],
                        description=exchange_record['description'],
                        private=exchange_record['private']
                    )
                    exchange.save()
        return exchange