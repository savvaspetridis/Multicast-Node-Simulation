'''
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
'''


from django.conf.urls import url

from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ex: /polls/
    url(r'^$', views.index, name='index'),
    url(r'^update$', views.get_ret_slide, name='get return slide'),
    # added for static
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root', settings.STATIC_ROOT}),


] 