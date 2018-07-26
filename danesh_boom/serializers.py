import re
from rest_framework import serializers
from rest_framework_jwt.serializers import JSONWebTokenSerializer, jwt_payload_handler, jwt_encode_handler
from django.contrib.auth.models import User

from users.models import Profile


class JWTSerializer(JSONWebTokenSerializer):
    def validate(self, attrs):
        credentials = {}
        username = attrs.get('username', None)
        pattern = re.compile('^[0][9][1][0-9]{8}$')
        if '@' in username:
            credentials['email'] = username
        elif pattern.match(username):
            credentials['auth_mobile'] = username
        else:
            credentials['username'] = username
        if credentials.get('auth_mobile', None) is None:
            try:
                user = User.objects.get(**credentials)
            except User.DoesNotExist:
                raise serializers.ValidationError("Unable to log in with provided credentials.")
        else:
            try:
                profile = Profile.objects.get(**credentials)
            except Profile.DoesNotExist:
                raise serializers.ValidationError("Unable to log in with provided credentials.")
            user = profile.profile_user

        if user.check_password(attrs.get('password')):
            payload = jwt_payload_handler(user)
            return {
                'token': jwt_encode_handler(payload),
                'user': user,
            }
        raise serializers.ValidationError("Unable to log in with provided credentials.")