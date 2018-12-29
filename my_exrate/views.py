from django.http import HttpResponse, HttpRequest
from .models import Question
from django.shortcuts import get_object_or_404, render
import requests
import re
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
    spisok_kursov = requests.get(url).text.split('},{')[1:-1]
    df = pd.DataFrame(columns=['Cur_ID', 'Date', 'Cur_Abbreviation', 'Cur_Scale', 'Cur_Name', 'Cur_OfficialRate'])
    for r_kurs in spisok_kursov:
        df.loc[r_kurs] = r_kurs.split(',')
    df.to_csv('file_rates', encoding='utf-8', index=False, index_label=True)
    df1 = pd.read_csv("file_rates")

    return HttpResponse(df1.to_html(table_id=None))


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'my_exrate/detail.html', {'question': question})
