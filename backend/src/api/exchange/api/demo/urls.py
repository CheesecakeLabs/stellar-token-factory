from django.urls import path

from . import views

urlpatterns = [
    path(
        "payees",
        views.get_payees_list,
        name="get-payees-list",
    )
]
