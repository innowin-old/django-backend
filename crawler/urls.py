from .views import export_research_gate_to_excel
from django.conf.urls import url

urlpatterns = [
    url(r'^topics/excel/', export_research_gate_to_excel, name='export_topics_excel'),
]