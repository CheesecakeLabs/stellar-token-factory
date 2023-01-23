from django.urls import path

from . import views

urlpatterns = [
    path(
        "payees",
        views.get_payees_list,
        name="get-payees-list",
    ),
    path(
        "balances/eur",
        views.get_main_wallet_eur_balance,
        name="get-main-wallet-eur-balance",
    ),
]
