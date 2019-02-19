from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Question, Valuta_kurs, Valuta
from django.shortcuts import get_object_or_404, render, render_to_response
from django.utils import translation
from django.utils.translation import LANGUAGE_SESSION_KEY, ugettext as _
import requests
import pandas as pd
import datetime as DT
import matplotlib.pyplot as plt
import re
import plotly.plotly as py
import plotly.graph_objs as go
import plotly

# import pickle
# from pymemcache import Client

now = DT.datetime.now()
today = DT.date.today()
week_ago = today - DT.timedelta(days=7)


def index(request):
    if request.user.is_authenticated and request.user.is_staff:
        username = request.user
        url = 'http://www.nbrb.by/API/ExRates/Rates?Periodicity=0'
        try:
            spisok_kursov = requests.get(url).json()
            # чтобы df.to_html не обрезал длинные строки до 50 символов
            pd.set_option('display.max_colwidth', -1)
            df = pd.DataFrame(spisok_kursov)
            # df.to_csv('file_rates.csv', encoding='utf-8', index=False, index_label=True)
            df1 = pd.DataFrame(columns=['amchart'])
            df2 = pd.DataFrame(columns=['matplotlib'])
            df3 = pd.DataFrame(columns=['plotly'])
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
                str_3 = '<a href="./' + str(
                    row_k[
                        'Cur_ID']) + '/plotly" target="_blank" id="but_plt" class ="badge badge-primary" style="width:50px">' + str(
                    row_k['Cur_Abbreviation']) + '</a>'
                df3 = df3.append({'plotly': str_3}, ignore_index=True)
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
            df['plotly'] = df3
            if request.LANGUAGE_CODE == 'ru':
                table_rates = df.to_html(escape=False, index=False, classes="table table-striped",
                                         columns=['Cur_ID', 'Cur_Abbreviation', 'Cur_Name', 'Cur_OfficialRate',
                                                  'Cur_Scale',
                                                  'amchart', 'matplotlib', 'plotly'])
            else:
                table_rates = df.to_html(escape=False, index=False, classes="table table-striped",
                                         columns=['Cur_ID', 'Cur_Abbreviation', 'Cur_OfficialRate',
                                                  'Cur_Scale',
                                                  'amchart', 'matplotlib', 'plotly'])
        except:
            table_rates = '<table border="1" class="dataframe table table-striped">  <thead>    <tr style="text-align: right;">      <th>Cur_ID</th>      <th>Cur_Abbreviation</th>      <th>Cur_Name</th>      <th>Cur_OfficialRate</th>      <th>Cur_Scale</th>      <th>amchart</th>      <th>matplotlib</th>    </tr>  </thead></table>'
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
    eml = 'ok'
    if re.search('^[a-z0-9_-]{3,16}$', request.POST.get('username')) == None:
        usr = 'user_not_check'
    if User.objects.filter(username=request.POST.get('username')).exists():
        usr = 'user_exists'

    if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z0-9]*$", request.POST.get('email')):
        eml = 'email_not_check'
    if User.objects.filter(email=request.POST.get('email')).exists():
        eml = 'email_exists'

    response = {'user': usr, 'email': eml}

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
    if request.user.is_authenticated:
        fig = plt.figure()
        ax = fig.add_subplot(111)
        for val_1 in Valuta.objects.filter(Cur_ID=Cur_ID):
            ax.set_title(val_1.Cur_Name)
            # for val_1 in Valuta.objects.all():
            x = []
            y = []
            for rate_1 in Valuta_kurs.objects.filter(Cur_ID=val_1.Cur_ID):
                x.append(DT.datetime(year=rate_1.Date.year, month=rate_1.Date.month, day=rate_1.Date.day))
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
        plt.savefig('my_exrate/static/image/foo.png')
        plt.close()
        # image_data = open("my_exrate/static/image/foo.png", "rb").read()
    else:
        return render_to_response('my_exrate/matplotlib.html', {})

    return render(request, 'my_exrate/matplotlib.html')


# построить график курсов  -- plotly
# import plotly
# plotly.tools.set_credentials_file(username='vitaly.by', api_key='T13Oh0V6SNXmdJK7rouH')
def plotly(request, Cur_ID):
    chartData = ""
    if request.user.is_authenticated:
        for val_1 in Valuta.objects.filter(Cur_ID=Cur_ID):
            x = []
            y = []
            for rate_1 in Valuta_kurs.objects.filter(Cur_ID=val_1.Cur_ID):
                x.append(DT.datetime(year=rate_1.Date.year, month=rate_1.Date.month, day=rate_1.Date.day))
                y.append(rate_1.Cur_OfficialRate)
            data = [go.Scatter(x=x, y=y)]
            py.plot(data, filename='plotly_chart', sharing='public', auto_open=False)
    else:
        return render_to_response('my_exrate/plotly.html', {})
    return render(request, 'my_exrate/plotly.html', {'header': val_1.Cur_Name})


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


def rate_by_week(request, Cur_ID):
    if request.user.is_authenticated and request.user.is_staff:
        username = request.user
        # кэширование
        # client = Client(('localhost', 11211))
        # table_rates = client.get('table_rates')
        # if table_rates is None:
        url = 'http://www.nbrb.by/API/ExRates/Rates/Dynamics/' + str(Cur_ID) + '?startDate=' + str(
            week_ago) + '&endDate=' + str(
            today)
        response = requests.get(url).json()
        # чтобы df.to_html не обрезал длинные строки до 50 символов
        pd.set_option('display.max_colwidth', -1)
        df = pd.DataFrame(response)
        str_3 = df["Cur_OfficialRate"].mean()
        df = df.append({'Cur_ID': '---', 'Cur_OfficialRate': str_3, 'Date': '---'}, ignore_index=True)

        table_rates = df.to_html(escape=False, index=False, classes='table table-striped')
    # кэширование
    #     client.set('table_rates', pickle.dumps(table_rates), expire=60)
    # else:
    #     table_rates = pickle.loads(table_rates)

    else:
        username = 'Аноним'
        table_rates = 'Вы не зарегистрированы или не имеете прав'

    return render_to_response('my_exrate/rate_by_week.html',
                              {'table': table_rates,
                               'user': username, 'login_form': request.user.is_authenticated})


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


def lang_change(request, lang_code):
    translation.activate(lang_code)
    request.session[LANGUAGE_SESSION_KEY] = lang_code
    my_string = _("Главная")
    print(my_string)
    # return render(request, 'my_exrate/index.html')
    return HttpResponseRedirect('/')


def server_upd(request):
    if request.POST.get('Cur_ID') is None or request.POST.get('Date') is None or request.POST.get(
            'Cur_OfficialRate') is None:
        status_upd = 'No input data'
    else:
        kurs_upd = Valuta_kurs.objects.filter(Cur_ID=request.POST.get('Cur_ID'),
                                              Date=request.POST.get('Date')).update(
            Cur_OfficialRate=request.POST.get('Cur_OfficialRate'))
        status_upd = 'OK'
        print(str(kurs_upd))
    print(status_upd)

    return JsonResponse({'status': status_upd})
