from django.urls import include, path

from .demo import urls as demo_urls
from .v1 import urls

urlpatterns = [path("v1/", include(urls)), path("payments/", include(demo_urls))]
