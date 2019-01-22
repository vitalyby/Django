from django.conf.urls import url
from . import views

app_name = 'my_exrate'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^my_exrate/$', views.index, name='index'),
    url(r'^login.html$', views.login_user, name='login'),
    url(r'^logout.html$', views.logout_user, name='logout'),
    url(r'^register$', views.register, name='register'),
    url(r'^register_user$', views.register_user, name='register'),
    url(r'^my_exrate/check_user$', views.check_user, name='check_user'),
    # url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'^(?P<Cur_ID>[0-9]+)/matplotlib', views.matplotlib, name='matplotlib'),
    # url(r'^my_exrate/amcharts/$', views.amcharts, name='amcharts'),
    url(r'^(?P<Cur_ID>[0-9]+)/amcharts$', views.amcharts, name='amcharts'),
    # url(r'^my_exrate/csv_file/$', views.csv_file, name='csv_file'),
    url(r'^my_exrate/select_rate/$', views.select_rate, name='select_rate'),
    url(r'^my_exrate/insert_rate/$', views.insert_rate, name='insert_rate'),
    url(r'^my_exrate/delete_rate/$', views.delete_rate, name='delete_rate'),
    url(r'^my_exrate/update_rate/$', views.update_rate, name='update_rate'),
]
