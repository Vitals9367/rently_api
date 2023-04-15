from django.contrib import admin
from django.urls import re_path, include
from django.http import HttpResponse


def healthz(*args, **kwargs):
    """Returns status code 200 if the server is alive."""
    return HttpResponse(status=200)


def readiness(*args, **kwargs):
    """
    Returns status code 200 if the server is ready to perform its duties.
    This goes through each database connection and perform a standard SQL
    query without requiring any particular tables to exist.
    """
    from django.db import connections

    for name in connections:
        cursor = connections[name].cursor()
        cursor.execute("SELECT 1;")
        cursor.fetchone()

    return HttpResponse(status=200)


urlpatterns = [
    re_path(r'^api/v1/', include('properties.urls')),
    re_path(r'^api/auth/', include('authentication.urls')),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    re_path(r'^healthz', healthz),
    re_path(r'^readiness', readiness),
]
