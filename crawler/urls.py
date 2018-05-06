from .views import export_research_gate_to_excel, export_vitrin_net_to_excel
from django.conf.urls import url

urlpatterns = [
    url(r'^topics/excel/', export_research_gate_to_excel, name='export_topics_excel'),
    url(r'^organizations/excel/', export_vitrin_net_to_excel, name='export_organizations_excel'),
]