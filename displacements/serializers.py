import psycopg2
import pprint

from rest_framework.serializers import ModelSerializer

from django.contrib.auth.models import User


class GetUserDataSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        print('salam')
        conn_string = "host='localhost' dbname='danesh_boom_test' user='postgres' password='1A2b3F4po'"
        # print the connection string we will use to connect
        print("Connecting to database\n	->%s" % conn_string)

        # get a connection, if a connect cannot be made an exception will be raised here
        conn = psycopg2.connect(conn_string)

        # conn.cursor will return a cursor object, you can use this cursor to perform queries
        cursor = conn.cursor()

        # execute our Query
        cursor.execute("SELECT * FROM auth_user")

        # retrieve the records from the database
        records = cursor.fetchall()
        pprint.pprint(records)