from django.conf.urls import url
from . import views

app_name = 'steamlist'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^results/([0-9]+)$', views.results, name='results'),

]
