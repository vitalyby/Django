from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'my_exrate'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'^graf/$', views.graf, name='graf'),
    url(r'^csv_file/$', views.csv_file, name='csv_file'),
    url(r'^select_rate/$', views.select_rate, name='select_rate'),
    url(r'^insert_rate/$', views.insert_rate, name='insert_rate'),
    url(r'^delete_rate/$', views.delete_rate, name='delete_rate'),
    url(r'^update_rate/$', views.update_rate, name='update_rate'),
]
