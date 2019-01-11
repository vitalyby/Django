from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Valuta_kurs, Valuta
from django.shortcuts import get_object_or_404, render
import requests
import pandas as pd
import datetime
import matplotlib.pyplot as plt

now = datetime.datetime.now()


def index(request):
    url = 'http://www.nbrb.by/API/ExRates/Rates?Periodicity=0'
    spisok_kursov = requests.get(url).json()
    df = pd.DataFrame(spisok_kursov)
    df.to_csv('file_rates', encoding='utf-8', index=False, index_label=True)
    for row_k in spisok_kursov:
        if Valuta.objects.filter(Cur_ID=row_k['Cur_ID']).exists() == False:
            kurs = Valuta(Cur_ID=row_k['Cur_ID'], Cur_Abbreviation=row_k['Cur_Abbreviation'],
                          Cur_Scale=row_k['Cur_Scale'], Cur_Name=row_k['Cur_Name'])
            kurs.save()
        if Valuta_kurs.objects.filter(Cur_ID_id=row_k['Cur_ID'], Date=row_k['Date']).exists() == False:
            val = Valuta_kurs(Cur_ID_id=row_k['Cur_ID'], Date=row_k['Date'],
                              Cur_OfficialRate=row_k['Cur_OfficialRate'])
            val.save()

    return HttpResponse(df.to_html(table_id=None))


# построить график курсов  -- amcharts
def amcharts(request):
    for val_1 in Valuta.objects.filter(Cur_ID=23):
        # for val_1 in Valuta.objects.all():
        x = []
        y = []
        for rate_1 in Valuta_kurs.objects.filter(Cur_ID=val_1.Cur_ID):
            x.append(rate_1.Date.isoformat())
            y.append(rate_1.Cur_OfficialRate)
        # x - Date y - Cur_OfficialRate label - Cur_Abbreviation
        plt.plot(x, y, label=val_1.Cur_Abbreviation)
        plt.legend(loc='right')  # так же указываем положение легенды
    plt.savefig('foo.png')
    image_data = open("foo.png", "rb").read()

    return render(request, 'my_exrate/amcharts.html', {'header': val_1.Cur_Abbreviation})


def graf(request):
    for val_1 in Valuta.objects.filter(Cur_ID=23):
        # for val_1 in Valuta.objects.all():
        x = []
        y = []
        for rate_1 in Valuta_kurs.objects.filter(Cur_ID=val_1.Cur_ID):
            x.append(rate_1.Date.isoformat())
            y.append(rate_1.Cur_OfficialRate)
        # x - Date y - Cur_OfficialRate label - Cur_Abbreviation
        plt.plot(x, y, label=val_1.Cur_Abbreviation)
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


def insert_rate(request):
    kurs_USD = Valuta.objects.filter(Cur_ID=145)[0]
    Valuta_kurs.objects.bulk_create([Valuta_kurs(Cur_ID=kurs_USD, Cur_OfficialRate=2.1123, Date=now.isoformat())])
    return HttpResponse(kurs_USD)


def select_rate(request):
    kurs_USD2 = Valuta_kurs.objects.filter(Cur_ID=145)
    return HttpResponse(kurs_USD2)


def delete_rate(request):
    kurs_USD3 = Valuta_kurs.objects.filter(Cur_ID=145, Cur_OfficialRate=2.1123).delete()
    return HttpResponse(kurs_USD3)


def update_rate(request):
    kurs_USD4 = Valuta_kurs.objects.filter(Cur_ID=145, Cur_OfficialRate=2.1123).update(Cur_OfficialRate=1.9999)
    return HttpResponse(kurs_USD4)


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
