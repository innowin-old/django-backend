import xlwt
from bs4 import BeautifulSoup
import requests
import string
from django.db import transaction
from django.http import HttpResponse

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


def export_research_gate_to_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="topics.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Topics')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['name']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Topic.objects.all().values_list('name')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


def crawl_vitrin_net():
    with transaction.atomic():
        organizations_entities = []
        print('start crawling ...')
        response = requests.get('https://vitrinnet.com/c/Food-industry-lines')
        soup = BeautifulSoup(response.content.decode('utf-8'), 'html.parser')
        categories = soup.find_all(name='a', attrs={'class': 'brand confirm'})
        # print(categories)
        for category in categories:
            organizations_url = 'https://vitrinnet.com/{0}'.format(category)
            orgaization_response = requests.get(organizations_url)
            organization_soup = BeautifulSoup(orgaization_response.content.decode('utf-8'), 'html.parser')
        data_resp = requests.post('https://vitrinnet.com/Handler/LoadContactInfo.ashx', data={'BrandId': 6393})
        print(data_resp.content)