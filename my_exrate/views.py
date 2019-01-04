from django.http import HttpResponse
from .models import Question, Valuta_kurs, Valuta
from django.shortcuts import get_object_or_404, render
import requests
import pandas as pd


def index(request):
    url = 'http://www.nbrb.by/API/ExRates/Rates?Periodicity=0'
    spisok_kursov = requests.get(url).json()
    df = pd.DataFrame(spisok_kursov)
    df.to_csv('file_rates', encoding='utf-8', index=False, index_label=True)
    for row_k in spisok_kursov:
        if Valuta.objects.filter(Cur_ID=row_k['Cur_ID']).exists() == False:
            kurs = Valuta(Cur_ID=row_k['Cur_ID'])
            kurs.save()
        if Valuta_kurs.objects.filter(Cur_ID_id=row_k['Cur_ID'], Date=row_k['Date']).exists() == False:
            val = Valuta_kurs(Cur_ID_id=row_k['Cur_ID'], Date=row_k['Date'], Cur_Abbreviation=row_k['Cur_Abbreviation'],
                              Cur_Scale=row_k['Cur_Scale'], Cur_Name=row_k['Cur_Name'],
                              Cur_OfficialRate=row_k['Cur_OfficialRate'])
            val.save()

    return HttpResponse(df.to_html(table_id=None))


def questions(request):
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


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'my_exrate/detail.html', {'question': question})
