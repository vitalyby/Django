from django.conf.urls import include, url

from . import views

urlpatterns = [
    # url(r'^my_exrate/', include('my_exrate.urls')),
    url(r'^$', views.index, name='index'),
]

