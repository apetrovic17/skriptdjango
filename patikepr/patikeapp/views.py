from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse('Probaaa')

def broj(request,br):
    return HttpResponse('Brojj: '+ str(br))
