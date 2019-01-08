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


# построить график курсов
def graf(request):
    import matplotlib.pyplot as plt

    # from matplotlib import rc
    import numpy as np
    # rc('font', family='Verdana')
    # url = 'http://www.nbrb.by/API/ExRates/Rates?Periodicity=0'
    # spisok_kursov = requests.get(url).json()
    # df = pd.DataFrame(spisok_kursov)
    # print(df.loc[df['Cur_ID'] == 170])
    # x = df.loc[df['Cur_ID'] == 170]
    x = 3
    plt.plot(x, x * 1.5, label='Первая линия')
    plt.plot(x, x * 3.0, label='Вторая декада')
    plt.plot(x, x / 3.0, label='Третья декада')
    plt.legend(loc='right')  # так же указываем положение легенды
    plt.savefig('foo.png')
    image_data = open("foo.png", "rb").read()

    return HttpResponse(image_data, content_type="image/png")


# скачать файл csv
def csv_file(request):
    import csv
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename = "file_rates"'
    writer = csv.writer(response)
    writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
    writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"'])

    return response


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
