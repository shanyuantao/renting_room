"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.views.static import serve

from project import settings

urlpatterns = [
    url(r'^app/', include('app.urls')),
    # url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),  # 配置这个用来DEBUG等于False的时候可以加载静态文件
    url(r'kaiapp/', include('kaiapp.urls', namespace='kaiapp')),
    url(r'^detail/', include('detail.urls')),
    url(r'^cwd/', include('cwdapp.urls')),
    # url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),  # 配置这个用来DEBUG等于False的时候可以加载静态文件
    # url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    # 配置这个用来DEBUG等于False的时候去加载静态图片
    # url(r'^$', views.home),  # 通过空匹配返回首页
    url(r'^xym/', include(('xym.urls', 'xym'), namespace='xym')),
]

from django.contrib.staticfiles.urls import static
from project import settings

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
