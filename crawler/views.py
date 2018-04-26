from django.shortcuts import render
from exchanges.models import Exchange


# Create your views here.
def crawl_research_gate():
    exchanges = Exchange.objects.all()
    print(exchanges)
    print('salam')