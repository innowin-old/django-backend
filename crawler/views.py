from bs4 import BeautifulSoup
import requests
import string
from django.db import transaction

from crawler.models import Topic


# Create your views here.
def crawl_research_gate():
    with transaction.atomic():
        topic_entities = []
        characters = list(string.ascii_uppercase)
        for character in characters:
            print('In page with character {0}'.format(character))
            response = requests.get('https://www.researchgate.net/topics/{0}'.format(character))
            soup = BeautifulSoup(response.content, 'html.parser')
            topics = soup.find_all(name='a', attrs={'class': 'js-score-goal'})
            for topic in topics:
                topic_entity = Topic(name=topic.get_text())
                topic_entities.append(topic_entity)
        print('Adding topics to database :))))))))))')
        Topic.objects.bulk_create(topic_entities)
        print('OK !')