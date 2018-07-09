from django.conf.urls import url, include
from django.contrib.staticfiles.urls import static
from project import settings

urlpatterns = [
    url(r'^shan/', include('shanyuantao.urls', namespace='shan'))
]


# 配置这个才能显示正确的路径显示图片
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)