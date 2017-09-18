from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^api/supervisor/$', views.supervisor_view),
    url(
        r'^api/supervisor/(?P<supervisor_id>.*?)/reload/$',
        views.supervisor_reload_view
    ),
    url(
        r'^api/supervisor/(?P<supervisor_id>.*?)/restart/$',
        views.supervisor_restart_view
    ),
    url(
        r'^api/supervisor/(?P<supervisor_id>.*?)/prog/$',
        views.supervisor_service_view
    ),
    url(
        r'^api/supervisor/(?P<supervisor_id>.*?)/prog/(?P<service_name>.*?)/stop/$',
        views.supervisor_service_stop_view
    ),
    url(
        r'^api/supervisor/(?P<supervisor_id>.*?)/prog/(?P<service_name>.*?)/start/$',
        views.supervisor_service_start_view
    ),
    url(
        r'^api/supervisor/(?P<supervisor_id>.*?)/prog/(?P<service_name>.*?)/stop/$',
        views.supervisor_service_restart_view
    ),
    url(
        r'^api/supervisor/(?P<supervisor_id>.*?)/prog/(?P<service_name>.*?)/console/$',
        views.supervisor_service_console_view
    ),
    url(
        r'^api/supervisor/(?P<supervisor_id>.*?)/prog/(?P<service_name>.*?)/stderr/$',
        views.supervisor_service_stderr_view
    )
]
