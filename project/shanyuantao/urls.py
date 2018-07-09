from django.conf.urls import url

from shanyuantao import views

urlpatterns = [
    url(r'^regist/', views.regist, name='regist'),
    url(r'^login/', views.login, name='login'),
    url(r'^area/', views.area, name='area'),
    url(r'^facility/', views.facilities, name='facility'),
    url(r'^house_type/', views.type_house, name='type'),

    url(r'^area_query_house/(\d+)/', views.area_query_house, name='area_query_house'),
    url(r'^price_query_house/(\d+)/(\d+)/', views.price_query_house, name='price_query_house'),
    url(r'^acreage_query_house/(\d+)/(\d+)/', views.acreage_query_house, name='acreage_query_house'),
    url(r'^type_query_house/(\d+)/', views.type_query_house, name='type_query_house'),

    url(r'^invest/', views.invest_jump, name='invest'),
    url(r'^myinvest/(\d+)/(\d+)/(\d+)/(\d+)/', views.invest_html, name='myinvest'),


]