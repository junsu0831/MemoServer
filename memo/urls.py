from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^top10/$', views.memo_top10, name='memo_top10'),
    url(r'^time/$', views.memo_time, name='memo_time'),
    url(r'^list/$', views.memo_list, name='memo_list'),
    url(r'^new/$', views.memo_new, name='memo_new'),
    url(r'^rest-api/$', views.memo_rest, name='memo_rest'),
]
