from django.urls import include, path

from .api import urls

app_name = "exchange"

urlpatterns = [path("api/", include(urls))]
