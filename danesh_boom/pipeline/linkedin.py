from users.models import Profile


def linkedin_pipe(backend, user, response, *args, **kwargs):
    if backend.name == 'linkedin-oauth2':
        if user.first_name == '' or user.first_name is None:
            user.first_name = response['firstName']

        if user.last_name == '' or user.last_name is None:
            user.last_name = response['lastName']

        if user.email == '' or user.email is None:
            user.email = response['emailAddress']

        try:
            user_profile = Profile.objects.get(profile_user=user)
        except Profile.DoesNotExist:
            return True
        if user_profile.linkedin_headline == '' or user_profile.linkedin_headline is None:
            user_profile.linkedin_headline = response['headline']

        if user_profile.social_image_url == '' or user_profile.social_image_url is None:
            user_profile.social_image_url = response['pictureUrl']

        if user_profile.linkedin_positions == '' or user_profile.linkedin_positions is None:
            user_profile.linkedin_positions = response['positions']
        user_profile.save()