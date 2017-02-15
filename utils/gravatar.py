import hashlib
import urllib


def get_gravatar_url(email, size=80):
    hash = hashlib.md5(email.lower().encode('utf-8')).hexdigest()
    gravatar_url = "https://www.gravatar.com/avatar/" + hash
    gravatar_url += "?" + urllib.parse.urlencode({'d': 'identicon', 'r': 'g', 's': str(size)})
    return gravatar_url
