from users.models import Profile
import requests


def yahoo_pipe(backend, user, response, *args, **kwargs):
    if backend.name == 'yahoo-oauth2':
        url = ' https://social.yahooapis.com/v1/user/{0}/contacts?format=json'.format(response['xoauth_yahoo_guid'])
        headers = {'Authorization': 'Bearer {0}'.format(response.get('access_token'))}
        contact_response = requests.get(url, headers=headers)
        print(contact_response.json())
        try:
            profile = Profile.objects.get(profile_user=user)
        except Profile.DoesNotExist:
            return True
        if profile.social_image_url == '' or profile.social_image_url is None:
            profile.social_image_url = response['image']['imageUrl']

        if profile.yahoo_contacts == '' or profile.yahoo_contacts is None:
            profile.yahoo_contacts = str(contact_response.json())

        profile.save()