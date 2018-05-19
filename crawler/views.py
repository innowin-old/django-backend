import xlwt
from bs4 import BeautifulSoup
import requests
import string
from django.db import transaction
from django.http import HttpResponse

from crawler.models import Topic, VitrinOrganization, ResearchGateTopic
from .category_lists import VITRINNET_CATEGORIES, RESEARCH_GATE_CHARACTER_BLACK_LIST


# Create your views here.
def crawl_research_gate():
    with transaction.atomic():
        topic_entities = []
        characters = list(string.ascii_uppercase)
        for character in characters:
            check_flag = True
            print('In page with character {0}'.format(character))
            response = requests.get('https://www.researchgate.net/topics/{0}'.format(character))
            soup = BeautifulSoup(response.content, 'html.parser')
            pager_container = soup.find(name='div', attrs={'class': 'c-list-navi pager'})
            if pager_container is not None:
                pages = pager_container.find_all(name='a')
                max_page = int(pages[len(pages)-2].get_text())
                for page_num in range(1, max_page+1):
                    if character in RESEARCH_GATE_CHARACTER_BLACK_LIST.keys():
                        if page_num <= RESEARCH_GATE_CHARACTER_BLACK_LIST[character]:
                            check_flag = False
                            print('page ' + str(page_num) + ' with character ' + character + ' not checked')
                        else:
                            check_flag = True
                    if check_flag:
                        print('In page ' + str(page_num) + ' with character ' + character)
                        response = requests.get('https://www.researchgate.net/topics/' + character + '/' + str(page_num))
                        soup = BeautifulSoup(response.content, 'html.parser')
                        topics = soup.find_all(name='a', attrs={'class': 'js-score-goal'})
                        for topic in topics:
                            topic_entity = ResearchGateTopic(name=topic.get_text())
                            topic_entities.append(topic_entity)
            else:
                topics = soup.find_all(name='a', attrs={'class': 'js-score-goal'})
                for topic in topics:
                    topic_entity = ResearchGateTopic(name=topic.get_text())
                    topic_entities.append(topic_entity)
        print('Adding topics to database :))))))))))')
        ResearchGateTopic.objects.bulk_create(topic_entities)
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

    rows = ResearchGateTopic.objects.all().values_list('name')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


def crawl_vitrin_net():
    categories = VITRINNET_CATEGORIES
    organizations_crawled = []
    with transaction.atomic():
        organizations_entities = []
        print('start crawling ...')
        for category in categories:
            print('in category ' + category)
            category_base_url = 'https://vitrinnet.com/c/{0}'.format(category)
            category_base_response = requests.get(category_base_url)
            category_base_soup = BeautifulSoup(category_base_response.content.decode('utf-8'), 'html.parser')
            pages_element = category_base_soup.find(name='ul', attrs={'id': 'InnerPage_PagingSec'})
            pages_num_in_base = len(pages_element.find_all(name='li'))
            if pages_num_in_base != 0:
                max_page_element = pages_element.find_all(name='li')[pages_num_in_base - 1]
                max_page_link = max_page_element.find(name='a')['href']
                max_page = max_page_link.split('/')[3]
                for page_num in range(1, int(max_page) + 1):
                    category_base_url = 'https://vitrinnet.com/c/' + category + '/' + str(page_num)
                    # print(category_base_url)
                    category_response = requests.get(category_base_url)
                    category_soup = BeautifulSoup(category_response.content.decode('utf-8'), 'html.parser')
                    organizations_name = category_soup.find_all(name='a', attrs={'class': 'brand'})
                    for organization_name in organizations_name:
                        print('in organization ' + organization_name['href'])
                        if organization_name['href'] in organizations_crawled:
                            print('this organizations added recently : ' + organization_name['href'])
                        else:
                            organization_url = 'https://vitrinnet.com{0}'.format(organization_name['href'])
                            organization_response = requests.get(organization_url)
                            organization_soup = BeautifulSoup(organization_response.content.decode('utf-8'),
                                                              'html.parser')
                            organization_loader = organization_soup.find(name='a', attrs={'id': 'LoadContactInfo'})
                            contact_resposne = requests.post('https://vitrinnet.com/Handler/LoadContactInfo.ashx',
                                                             data={'BrandId': organization_loader['data-brandinfoid']})
                            contact_soup = BeautifulSoup(contact_resposne.content.decode('utf-8'), 'html.parser')
                            organization_object = VitrinOrganization(name=organization_soup.find(name='h1').get_text(),
                                                                     internal_link=organization_name['href'])
                            a_tags = contact_soup.find_all(name='a')
                            for a_tag in a_tags:
                                contact_type = a_tag.find(name='i')
                                if 'fa-phone' in contact_type['class']:
                                    organization_object.phone = a_tag.get_text()
                                elif 'fa-external-link' in contact_type['class']:
                                    organization_object.website = a_tag.get_text()
                                elif 'fa-telegram' in contact_type['class']:
                                    organization_object.telegram_link = a_tag.get_text()
                                elif 'fa-mobile' in contact_type['class']:
                                    organization_object.mobile = a_tag.get_text()
                                elif 'fa-instagram' in contact_type['class']:
                                    organization_object.instagram_link = a_tag.get_text()
                            organization_object.save()
                            '''organizations_entities.append(organization_object)'''
                            organizations_crawled.append(organization_name['href'])
                    print(category_base_url + 'data added to array !')
            else:
                category_url = 'https://vitrinnet.com/c/{0}'.format(category)
                category_response = requests.get(category_url)
                category_soup = BeautifulSoup(category_response.content.decode('utf-8'), 'html.parser')
                organizations_name = category_soup.find_all(name='a', attrs={'class': 'brand'})
                for organization_name in organizations_name:
                    print('in organization ' + organization_name['href'])
                    if organization_name['href'] in organizations_crawled:
                        print('this organizations added recently : ' + organization_name['href'])
                    else:
                        organization_url = 'https://vitrinnet.com{0}'.format(organization_name['href'])
                        organization_response = requests.get(organization_url)
                        organization_soup = BeautifulSoup(organization_response.content.decode('utf-8'), 'html.parser')
                        organization_loader = organization_soup.find(name='a', attrs={'id': 'LoadContactInfo'})
                        contact_resposne = requests.post('https://vitrinnet.com/Handler/LoadContactInfo.ashx',
                                                         data={'BrandId': organization_loader['data-brandinfoid']})
                        contact_soup = BeautifulSoup(contact_resposne.content.decode('utf-8'), 'html.parser')
                        organization_object = VitrinOrganization(name=organization_soup.find(name='h1').get_text(),
                                                                 internal_link=organization_name['href'])
                        a_tags = contact_soup.find_all(name='a')
                        for a_tag in a_tags:
                            contact_type = a_tag.find(name='i')
                            if 'fa-phone' in contact_type['class']:
                                organization_object.phone = a_tag.get_text()
                            elif 'fa-external-link' in contact_type['class']:
                                organization_object.website = a_tag.get_text()
                            elif 'fa-telegram' in contact_type['class']:
                                organization_object.telegram_link = a_tag.get_text()
                            elif 'fa-mobile' in contact_type['class']:
                                organization_object.mobile = a_tag.get_text()
                            elif 'fa-instagram' in contact_type['class']:
                                organization_object.instagram_link = a_tag.get_text()
                        organization_object.save()
                        '''organizations_entities.append(organization_object)'''
                        organizations_crawled.append(organization_name['href'])
                print(category_url + 'data added to array !')
        print('Adding organizations to database :))))))))))')
        print('OK !')


def export_vitrin_net_to_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="organizations.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Organizations')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['name', 'phone', 'mobile', 'website', 'telegram_link', 'instagram_link']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = VitrinOrganization.objects.all().values_list('name', 'phone', 'mobile', 'website', 'telegram_link', 'instagram_link')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response