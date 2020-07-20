from django.conf.urls import include, url
from . import views


urlpatterns = [
    url(r'^(?P<id>[0-9]+)/$', views.CharacterAPIView.as_view(), name='get-character'),
    url(r'^(?P<id>[0-9]+)/rating/$', views.CharacterAPIView.as_view(), name='post-character'),
    # Una mejora aqui es configurar de tal manera de capturar todas las URL's que no entren por los
    # endpoints declarados
]