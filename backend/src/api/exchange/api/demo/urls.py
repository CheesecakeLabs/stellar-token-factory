from django.urls import path

from . import views

urlpatterns = [
    path(
        "payees",
        views.get_payees_list,
        name="get-payees-list",
    ),
    path(
        "path-payment-strict-receive",
        views.create_path_payment_strict_receive_envelope,
        name="path-payment-strict-receive",
    ),
    path(
        "balances/eur",
        views.get_main_wallet_eur_balance,
        name="get-main-wallet-eur-balance",
    ),
    path(
        "submit",
        views.submit_envelope,
        name="submit-envelope-path-payment",
    ),
]
