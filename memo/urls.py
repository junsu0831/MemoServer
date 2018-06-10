from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.memo_list, name='memo_list'),
    url(r'^new/$', views.memo_new, name='memo_new'),
]
