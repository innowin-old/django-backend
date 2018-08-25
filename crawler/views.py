import xlwt
from bs4 import BeautifulSoup
import requests
import string
from django.db import transaction
from django.http import HttpResponse

from .models import VitrinOrganization, ResearchGateTopic, SkillemaTags, IctMotherOrganization, IctExpert
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


def normalize_research_gate_data():
    topics = ResearchGateTopic.objects.filter()
    for topic in topics:
        topic_repeated_names = ResearchGateTopic.objects.filter(name=topic.name)
        if topic_repeated_names.count() > 1:
            print(str(topic_repeated_names[1].name) + ' deleted !')
            topic_repeated_names[1].delete()
    print('Repeated names deleted successfully !')


def research_gate_all_flag_true():
    topics = ResearchGateTopic.objects.all()
    for topic in topics:
        topic.delete_flag = False
        topic.save()
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


def get_ictstartups_expert():
    base_url = 'http://www.ictstartups.ir'
    with transaction.atomic():
        for i in range(1, 64):
            expert_url = base_url + '/fa/profile/list/expert/{0}'.format(i)
            expert_response = requests.get(expert_url)
            expert_soup = BeautifulSoup(expert_response.content.decode('utf-8'), 'html.parser')
            expert_elements = expert_soup.find_all(name='a', attrs={'class': 'linkPicTitle'})
            for expert_element in expert_elements:
                expert_page_url = base_url + expert_element['href']
                expert_page_content = requests.get(expert_page_url)
                expert_page_soup = BeautifulSoup(expert_page_content.content.decode('utf-8'), 'html.parser')
                expert_container = expert_page_soup.find(name='section', attrs={'class': 'Specifications mui-col-md-10 '})
                expert_rows = expert_container.find_all(name='div', attrs={'class': 'mui-row'})
                expert_name = expert_page_soup.find(name='h1', attrs={'id': 'lblName'})
                expert_data = {'name': expert_name.text}
                print('adding : ' + str(expert_data['name']))
                for expert_row in expert_rows:
                    expert_divs = expert_row.find_all(name='div')
                    for expert_div in expert_divs:
                        label = expert_div.find(name='label')
                        span = expert_div.find(name='span')
                        if span is None:
                            span = expert_div.find(name='a')
                        if label is not None:
                            if label.text.strip() == 'مدرک تحصیلی: '.strip():
                                # print('site address : ' + span.text)
                                expert_data['education'] = str(span.text)
                            elif label.text.strip == 'کشور:'.strip():
                                # print('site phone : ' + span.text)
                                expert_data['country'] = str(span.text)
                            elif label.text.strip() == 'استان:'.strip():
                                # print('site email : ' + span.text)
                                expert_data['province'] = str(span.text)
                            elif label.text.strip() == 'شهر:'.strip():
                                # print('site country : ' + span.text)
                                expert_data['town'] = str(span.text)
                            elif label.text.strip() == 'آدرس محل‌کار: '.strip():
                                # print('site province : ' + span.text)
                                expert_data['work_address'] = str(span.text)
                            elif label.text.strip() == ' معرفی‌: '.strip():
                                # print('site town : ' + span.text)
                                expert_data['description'] = str(span.text)
                IctExpert.objects.create(**expert_data)
                expert_data = {}
    print('Done !!!')


def export_ictstartups_expert(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="ict_experts.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('IctExperts')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['name', 'education', 'country', 'province', 'town', 'work_address', 'description']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = IctExpert.objects.all().values_list('name', 'education', 'country', 'province', 'town', 'work_address', 'description')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


def get_ictstartups_organization():
    base_url = 'http://www.ictstartups.ir'
    for i in range(1, 31):
        organization_url = base_url + '/fa/company/list/companies/{0}'.format(i)
        organization_response = requests.get(organization_url)
        organization_soup = BeautifulSoup(organization_response.content.decode('utf-8'), 'html.parser')
        organization_elements = organization_soup.find_all(name='a', attrs={'class': 'linkPicTitle'})
        for organization_element in organization_elements:
            organization_page_url = base_url + organization_element['href']
            organization_page_content = requests.get(organization_page_url)
            organization_page_soup = BeautifulSoup(organization_page_content.content.decode('utf-8'), 'html.parser')
            organization_container = organization_page_soup.find(name='div', attrs={'class': 'Specifications mui-col-md-9'})
            organization_rows = organization_container.find_all(name='div', attrs={'class': 'mui-row'})
            organization_name = organization_page_soup.find(name='h1', attrs={'class': 'companyName'})
            organization_data = {'name': organization_name.text}
            for organization_row in organization_rows:
                organization_divs = organization_row.find_all(name='div')
                for organization_div in organization_divs:
                    label = organization_div.find(name='label')
                    span = organization_div.find(name='span')
                    if span is None:
                        span = organization_div.find(name='a')
                    if label is not None:
                        if label.text.strip() == 'آدرس سایت: '.strip():
                            # print('site address : ' + span.text)
                            organization_data['web_site'] = str(span.text)
                        elif label.text.strip == 'شماره تماس:'.strip():
                            # print('site phone : ' + span.text)
                            organization_data['phone'] = str(span.text)
                        elif label.text.strip() == 'پست‌الکترونیک:'.strip():
                            # print('site email : ' + span.text)
                            organization_data['email'] = str(span.text)
                        elif label.text.strip() == 'کشور:'.strip():
                            # print('site country : ' + span.text)
                            organization_data['country'] = str(span.text)
                        elif label.text.strip() == 'استان:'.strip():
                            # print('site province : ' + span.text)
                            organization_data['province'] = str(span.text)
                        elif label.text.strip() == 'شهر:'.strip():
                            # print('site town : ' + span.text)
                            organization_data['town'] = str(span.text)
                        elif label.text.strip() == 'معرفی کوتاه:'.strip():
                            # print('site description : ' + span.text)
                            organization_data['description'] = str(span.text)
            IctMotherOrganization.objects.create(**organization_data)
            organization_data = {}
    print('Done !!!')


def export_ictstartups_organization(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="ict_organizations.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('IctOrganizations')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['name', 'web_site', 'phone', 'email', 'country', 'province', 'town', 'description']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = IctMotherOrganization.objects.all().values_list('name', 'web_site', 'phone', 'email', 'country', 'province', 'town', 'description')
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
                            contact_response = requests.post('https://vitrinnet.com/Handler/LoadContactInfo.ashx',
                                                             data={'BrandId': organization_loader['data-brandinfoid']})
                            contact_soup = BeautifulSoup(contact_response.content.decode('utf-8'), 'html.parser')
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


def fetch_skillema_tags():
    url = 'https://www.skillema.ir/api/tags/lists'
    resp = requests.get(url=url)
    json_tags = resp.json()
    print(len(json_tags))
    # add all tags to database
    for json_tag in json_tags:
        try:
            tag = SkillemaTags.objects.get(name=json_tag.get('name'))
        except SkillemaTags.DoesNotExist:
            tag = SkillemaTags.objects.create(name=json_tag.get('name'),
                                              created_at=json_tag.get('created_at'),
                                              updated_at=json_tag.get('updated_at'))
        tag.save()
    print('tags added to database !')
    # set tag relations
    for json_tag in json_tags:
        try:
            tag = SkillemaTags.objects.get(name=json_tag.get('name'))
        except SkillemaTags.DoesNotExist:
            tag = None
            print('tag not found !')
        if tag is not None:
            json_find_flag = False
            for json_tag_parent in json_tags:
                if json_tag_parent.get('id') == json_tag.get('parent_id'):
                    json_find_flag = True
                    try:
                        tag_parent = SkillemaTags.objects.get(name=json_tag_parent.get('name'))
                    except SkillemaTags.DoesNotExist:
                        tag_parent = None
                        print('parent tag not found !')
                    if tag_parent is not None:
                        tag.parent = tag_parent
                        tag.save()
            if not json_find_flag:
                print('parent tag not found in json')
    print('success !')


def export_skillema_tags_to_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="skillema-tags.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('SkillemaTags')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['id', 'name', 'created_at', 'updated_at', 'parent_id']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = SkillemaTags.objects.all().values_list('id', 'name', 'created_at', 'updated_at', 'parent_id')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response