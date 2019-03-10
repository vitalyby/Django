from django.conf.urls import url
from . import views
from django.views.generic import RedirectView

app_name = 'my_exrate'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^my_exrate/$', views.index, name='index'),
    url(r'^login$', views.user_login, name='user_login'),
    url(r'^logout$', views.user_logout, name='user_logout'),
    url(r'^register$', views.register, name='register'),
    url(r'^(?P<lang_code>[a-z]{2})$', views.lang_change, name='lang_change'),
    url(r'^user_register$', views.user_register, name='user_register'),
    url(r'^user_check$', views.user_check, name='user_check'),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/image/favicon.ico')),
    # url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'^(?P<Cur_ID>[0-9]+)/matplotlib', views.matplotlib, name='matplotlib'),
    url(r'^(?P<Cur_ID>[0-9]+)/plotly', views.plotly, name='plotly'),
    url(r'^(?P<Cur_ID>[0-9]+)/rate_by_week', views.rate_by_week, name='rate_by_week'),
    url(r'^rate_by_day$', views.rate_by_day, name='rate_by_day'),
    # url(r'^my_exrate/amcharts/$', views.amcharts, name='amcharts'),
    url(r'^(?P<Cur_ID>[0-9]+)/amcharts$', views.amcharts, name='amcharts'),
    # url(r'^my_exrate/csv_file/$', views.csv_file, name='csv_file'),
    url(r'^my_exrate/rate_select/$', views.rate_select, name='rate_select'),
    url(r'^my_exrate/rate_insert/$', views.rate_insert, name='rate_insert'),
    url(r'^my_exrate/rate_delete/$', views.rate_delete, name='rate_delete'),
    url(r'^my_exrate/rate_update/$', views.rate_update, name='rate_update'),
    url(r'^server_upd$', views.server_upd, name='server_upd'),
]
