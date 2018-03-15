import psycopg2
from psycopg2.extras import DictCursor

from rest_framework.serializers import ModelSerializer, ListField

from django.contrib.auth.models import User
from django.conf import settings
from users.models import Profile, Identity


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