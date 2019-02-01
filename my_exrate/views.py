from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Question, Valuta_kurs, Valuta
from django.shortcuts import get_object_or_404, render, render_to_response
import requests
import pandas as pd
import datetime
import matplotlib.pyplot as plt

now = datetime.datetime.now()


def index(request):
    if request.user.is_authenticated and request.user.is_staff:
        username = request.user
        url = 'http://www.nbrb.by/API/ExRates/Rates?Periodicity=0'
        spisok_kursov = requests.get(url).json()
        # чтобы df.to_html не обрезал длинные строки до 50 символов
        pd.set_option('display.max_colwidth', -1)
        df = pd.DataFrame(spisok_kursov)
        # df.to_csv('file_rates', encoding='utf-8', index=False, index_label=True)
        df1 = pd.DataFrame(columns=['amchart'])
        df2 = pd.DataFrame(columns=['matplotlib'])
        for row_k in spisok_kursov:
            str_1 = '<a href="./' + str(
                row_k[
                    'Cur_ID']) + '/amcharts" target="_blank" id="but_am" class ="badge badge-primary" style="width:50px">' + str(
                row_k['Cur_Abbreviation']) + '</a>'
            df1 = df1.append({'amchart': str_1}, ignore_index=True)
            str_2 = '<a href="./' + str(
                row_k[
                    'Cur_ID']) + '/matplotlib" target="_blank" id="but_mat" class ="badge badge-primary" style="width:50px">' + str(
                row_k['Cur_Abbreviation']) + '</a>'
            df2 = df2.append({'matplotlib': str_2}, ignore_index=True)
            if Valuta.objects.filter(Cur_ID=row_k['Cur_ID']).exists() == False:
                kurs = Valuta(Cur_ID=row_k['Cur_ID'],
                              Cur_Abbreviation=row_k['Cur_Abbreviation'],
                              Cur_Scale=row_k['Cur_Scale'],
                              Cur_Name=row_k['Cur_Name'])
                kurs.save()
            if Valuta_kurs.objects.filter(Cur_ID_id=row_k['Cur_ID'],
                                          Date=row_k['Date']).exists() == False:
                val = Valuta_kurs(Cur_ID_id=row_k['Cur_ID'], Date=row_k['Date'],
                                  Cur_OfficialRate=row_k['Cur_OfficialRate'])
                val.save()
        df['amchart'] = df1
        df['matplotlib'] = df2
        table_rates = df.to_html(escape=False, index=False, classes="table table-striped",
                                 columns=['Cur_ID', 'Cur_Abbreviation', 'Cur_Name', 'Cur_OfficialRate', 'Cur_Scale',
                                          'amchart', 'matplotlib'])
    else:
        username = 'Аноним'
        table_rates = 'Вы не зарегистрированы или не имеете прав'

    return render_to_response('my_exrate/index.html',
                              {'table': table_rates,
                               'user': username, 'login_form': request.user.is_authenticated})


def user_login(request):
    user = authenticate(username=request.POST.get('username'),
                        password=request.POST.get('password'))
    if user is None:
        return render_to_response('my_exrate/login.html', {})
    else:
        login(request, user)

    return HttpResponseRedirect('/')


def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return HttpResponseRedirect('/')


def register(request):
    return render_to_response('my_exrate/register.html')


def user_register(request):
    user = User.objects.create_user(username=request.POST.get('username'), email=request.POST.get('email'),
                                    password=request.POST.get('password'), is_staff=True)
    login(request, user)
    return HttpResponseRedirect('/')


def user_check(request):
    usr = 'ok'
    if User.objects.filter(username=request.POST.get('username')).exists():
        usr = 'user_exists'
    response = {'user': usr}
    return JsonResponse(response)


# построить график курсов  -- amcharts
def amcharts(request, Cur_ID):
    chartData = ""
    if request.user.is_authenticated:
        # if request.user.is_authenticated and request.user.view('my_exrate.valuta'):
        for val_1 in Valuta.objects.filter(Cur_ID=Cur_ID):
            # for val_1 in Valuta.objects.all():
            x = []
            y = []
            i = 0
            quot = "\""
            for rate_1 in Valuta_kurs.objects.filter(Cur_ID=val_1.Cur_ID):
                # chartData += prefix
                chartData += "{\n"
                chartData += "date:" + quot + str(rate_1.Date.year) + "-" + str(
                    '{:02d}'.format(rate_1.Date.month)) + "-" + str(
                    '{:02d}'.format(rate_1.Date.day)) + quot + ",\n"
                chartData += "value:" + str(rate_1.Cur_OfficialRate) + "\n}"
                i = i + 1
                chartData += ","
                # print(chartData)
    else:
        return render_to_response('my_exrate/amcharts.html', {})
    return render(request, 'my_exrate/amcharts.html', {'header': val_1.Cur_Name, 'chartData': chartData})


# построить график курсов  -- matplotlib
def matplotlib(request, Cur_ID):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    for val_1 in Valuta.objects.filter(Cur_ID=Cur_ID):
        ax.set_title(val_1.Cur_Name)
        # for val_1 in Valuta.objects.all():
        x = []
        y = []
        for rate_1 in Valuta_kurs.objects.filter(Cur_ID=val_1.Cur_ID):
            x.append(datetime.datetime(year=rate_1.Date.year, month=rate_1.Date.month, day=rate_1.Date.day))
            y.append(rate_1.Cur_OfficialRate)
        # x - Date y - Cur_OfficialRate label - Cur_Abbreviation
        ax.plot(x, y, label=val_1.Cur_Abbreviation)
        ax.legend(loc='lower right')  # так же указываем положение легенды
    for label in ax.xaxis.get_ticklabels():
        # цвет подписи деленений оси OX
        label.set_color('blue')
        # поворот подписей деленений оси OX
        label.set_rotation(30)
        # размер шрифта подписей делений оси OX
        label.set_fontsize(8)
    plt.savefig('foo.png')
    plt.close()
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


def rate_insert(request):
    kurs_USD = Valuta.objects.filter(Cur_ID=145)[0]
    Valuta_kurs.objects.bulk_create([Valuta_kurs(Cur_ID=kurs_USD,
                                                 Cur_OfficialRate=2.1123,
                                                 Date=now.isoformat())])
    return HttpResponse(kurs_USD)


def rate_select(request):
    kurs_USD2 = Valuta_kurs.objects.filter(Cur_ID=145)
    return HttpResponse(kurs_USD2)


def rate_delete(request):
    kurs_USD3 = Valuta_kurs.objects.filter(Cur_ID=145,
                                           Cur_OfficialRate=2.1123).delete()
    return HttpResponse(kurs_USD3)


def rate_update(request):
    kurs_USD4 = Valuta_kurs.objects.filter(Cur_ID=145,
                                           Cur_OfficialRate=2.1123).update(
        Cur_OfficialRate=1.9999)
    return HttpResponse(kurs_USD4)


def questions(request):
    latest_question_list = Question.objects.order_by('id')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'my_exrate/index.html', context)


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'my_exrate/detail.html', {'question': question})


def test_fn1(ls, divisor):
    result = []
    idx = 0
    while idx < len(ls):
        result.append(ls[idx] / divisor)
        idx = idx + 1
    return result
