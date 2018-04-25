from users.models import Profile


def google_pipe(backend, user, response, *args, **kwargs):
    if backend.name == 'google-oauth2':
        try:
            profile = Profile.objects.get(profile_user=user)
        except Profile.DoesNotExist:
            return True
        if user.first_name == '' or user.first_name is None:
            user.first_name = response['name']['givenName']
        if user.last_name == '' or user.last_name is None:
            user.last_name = response['name']['familyName']
        user.save()
        profile.gender = response['gender']
        profile.is_plus_user = response['isPlusUser']
        profile.google_plus_address = response['url']
        if not response['image']['isDefault']:
            profile.google_plus_image = response['image']['url']
        profile.save()
