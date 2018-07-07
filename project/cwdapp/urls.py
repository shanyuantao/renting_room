from cwdapp import views
from django.conf.urls import url

urlpatterns = [
    url('^index/', views.Index),
    url('^myself/', views.My_self),
    url('^change_pas/', views.Change_password),
    url('^like/', views.I_like),
    url('^ture/', views.Ture_name),
    url('^myhouse/', views.My_house),
    url('^l/', views.login),
]
