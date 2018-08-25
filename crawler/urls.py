from .views import export_research_gate_to_excel, export_vitrin_net_to_excel, export_skillema_tags_to_excel, export_ictstartups_organization, export_ictstartups_expert
from django.conf.urls import url

urlpatterns = [
    url(r'^topics/excel/', export_research_gate_to_excel, name='export_topics_excel'),
    url(r'^organizations/excel/', export_vitrin_net_to_excel, name='export_organizations_excel'),
    url(r'^skillema-tags/excel/', export_skillema_tags_to_excel, name='export_skillema_tags_to_excel'),
    url(r'^ict-organizations/excel/', export_ictstartups_organization, name='export_ictstartups_organization_to_excel'),
    url(r'^ict-experts/excel/', export_ictstartups_expert, name='export_ictstartups_expert_to_excel')
]