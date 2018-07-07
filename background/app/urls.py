from django.conf.urls import url

from app import views


urlpatterns = [
    url('^hello/', views.hello),
    url('^adminlogin/', views.adminlogin),
    url('^adminlogout/', views.adminlogout),
    url('^refresh/', views.refresh),
    url('^update_pwd/',views.update_pwd),
    url('^house_manage/(\d+)/', views.house_manage),
    url('^system/', views.system),
    url('^del_house/(\d+)/(\d+)/',views.del_house),
    url('^edit_house/(\d+)/(\d+)/', views.edit_house)

]