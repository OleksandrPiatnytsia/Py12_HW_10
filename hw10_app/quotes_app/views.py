from django.shortcuts import render

from django.http import HttpResponse


def index(request):
    return render(request, "quotes_app/index.html", context={"title": "Quotes app main"})