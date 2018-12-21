from django.http import HttpResponse, HttpRequest
from .models import Question
from django.shortcuts import get_object_or_404, render
import requests
import pandas as pd


# def index(request):
#     return HttpResponse("Hello, world.")
def index(request):
    latest_question_list = Question.objects.order_by('id')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'my_exrate/index.html', context)


def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)

def rate(request, question_id):
    url = 'http://www.nbrb.by/API/ExRates/Rates?Periodicity=0'
    # tables = pd.read_html(requests.get(url).text, header=0)
    a = requests.get(url).text
    b = pd.Series(a)

    return HttpResponse("выводим массив \n %s." % b)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'my_exrate/detail.html', {'question': question})
