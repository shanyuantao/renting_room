from django.conf.urls import url
from detail import views


urlpatterns = [
    url(r'^detail/(\d+)/', views.detail),
    url(r'^collect/', views.collect),
]
