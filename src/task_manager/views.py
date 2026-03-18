from django.shortcuts import render

from django.http import HttpResponse

#MTV
def index(request):
    return HttpResponse("Hello, world.")
