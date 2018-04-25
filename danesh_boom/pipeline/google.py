from users.models import Profile


def google_pipe(backend, user, response, *args, **kwargs):
    if backend.name == 'google-oauth2':
        try:
            user_profile = Profile.objects.get(profile_user=user)
        except Profile.DoesNotExist:
            return True

        if user.first_name == '' or user.first_name is None:
            user.first_name = response['name']['givenName']

        if user.last_name == '' or user.last_name is None:
            user.last_name = response['name']['familyName']

        user.save()
        user_profile.gender = response['gender']
        user_profile.is_plus_user = response['isPlusUser']
        user_profile.google_plus_address = response['url']
        if not response['image']['isDefault']:
            user_profile.social_image_url = response['image']['url']

        user_profile.save()
