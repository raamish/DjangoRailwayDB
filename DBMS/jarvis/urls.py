import views
from django.conf.urls import url

urlpatterns = [ url(r'^signup/$',views.signup), url(r'^login/$', views.login),
    #url(r'^signup_confirm$', views.signup_confirm)
    url(r'^dashboard/$', views.dashboard),
    url(r'^history/$', views.history),
    url(r'^enqj/$', views.enqj),
    url(r'^enqt/$', views.enqt),
    url(r'^cancel/$', views.cancel),
    url(r'^booking/$', views.booking),
    url(r'^booktrain/$',views.booktrain)
    ]